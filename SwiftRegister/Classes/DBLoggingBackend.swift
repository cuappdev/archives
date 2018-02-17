import Foundation
import RealmSwift
import PromiseKit

class DBEventItem : Object {
    @objc dynamic var serializedLog: JSONData = Data()
    @objc dynamic var eventName: String = ""
    @objc dynamic var identifier: String = ""
    @objc dynamic var timestamp: Date = Date()
    
    ///this is true when the event is being sent. Should clear out all objects
    ///with isSending = true after successfuly sending events
    @objc dynamic var isSending: Bool = false
    
    override class func primaryKey() -> String? {
        return "identifier"
    }
}

enum DBLoggingError: Error {
    case realmFailedToCreate(reason: String), sessionDeallocated, noEventSender
    case failedToSendEventsToServer
}

private enum DBLoggingInternError: Error {
    case alreadySendingError
}

//TODO need to revamp the scheduled uploading system
// - background uploading
// - possibly use something besides NSTimer to reduce energy consumption (like gcd maybe)
// - If we use NSTimer, should we use a run loop besides RunLoop.main?
//TODO need delegate functions to notify when events are sent to the server
class DBLoggingBackend {
    
    private var sendTimer: Timer?
    private weak var eventSender: EventSender?
    let syncQueue: DispatchQueue
    private var isSendingEvents: Bool = false // use syncQueue before accessing
    private let timerInterval: TimeInterval
    
    typealias EventsSentCallback = () -> ()
    private var _onEventsSent: EventsSentCallback?
    
    /**
     * Gets called when events are sent.
     * Setting/getting is thread-safe *and may block*.
     */
    var onEventsSent: EventsSentCallback? {
        set {
            syncQueue.sync { _onEventsSent = newValue }
        }
        get {
            return syncQueue.sync { _onEventsSent }
        }
    }
    
    init(eventSender: EventSender, timerInterval: TimeInterval = 10) {
        self.timerInterval = timerInterval
        self.eventSender = eventSender
        self.syncQueue = DispatchQueue.init(label: "register.db_logging_backend")
    }
    
    static func makeRealm() throws -> Realm {
        let realmConfig = Realm.Configuration(
            fileURL: URL.init(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("register.realm")
        )
        do {
            return try Realm(configuration: realmConfig)
        } catch let e {
            throw DBLoggingError.realmFailedToCreate(reason: e.localizedDescription)
        }
    }
    
    @discardableResult
    func logEvent<T>(event: Event<T>) -> Promise<()> {
        return Promise { fulfill, reject in
            let randTag = arc4random()
            let timestampedEvent = TimestampedEvent(event: event)
            
            let dbEvent = DBEventItem()
            dbEvent.serializedLog = try timestampedEvent.serializeJson()
            dbEvent.eventName = timestampedEvent.eventName
            //TODO should probably generate ids differently
            dbEvent.identifier = "\(event.eventName):\(timestampedEvent.timestamp.timeIntervalSince1970):\(randTag)"
            dbEvent.timestamp = timestampedEvent.timestamp
            
            let realm = try DBLoggingBackend.makeRealm()
            
            try realm.write {
                realm.add(dbEvent)
            }
            
            scheduleEventSend(interval: timerInterval)

            fulfill(())
        }.catch { err in
            registerLogger.error("Failed to log an event with name \(event.eventName)")
            registerLogger.error(err)
        }
    }
    
    /**
     * Schedules a timer to send events in `interval` seconds. Thread safe.
     */
    func scheduleEventSend(interval: TimeInterval) {
        self.syncQueue.async {
            //make sure there isn't currently a timer running.
            guard self.sendTimer == nil else {
                return
            }
            
            let timer = Timer.init(timeInterval: interval, repeats: false, block: {[weak self] _ in
                self?.sendAllEvents()
                self?.sendTimer?.invalidate()
                self?.sendTimer = nil
            })
            RunLoop.main.add(timer, forMode: RunLoopMode.commonModes)
            
            self.sendTimer = timer
            
        }
    }
    
    /**
     * Tries to send events immediately using the event sender. If the event is currently being sent already,
     * throw a DBLoggingInternError.alreadySendingError.
     */
    @discardableResult
    func sendAllEvents() -> Promise<()> {
        return Promise(value: ())
        .then(on: syncQueue) { () -> [JSONData] in
            if self.isSendingEvents {
                throw DBLoggingInternError.alreadySendingError
            } else {
                self.isSendingEvents = true
            }
            
            //synchronously get events from db and mark each event with isSending = true
            let realm = try DBLoggingBackend.makeRealm()
            let logs = Array(realm.objects(DBEventItem.self))
            try realm.write {
                logs.forEach {$0.isSending = true}
            }
            let data = logs.map {$0.serializedLog}
            return data
        }.then(on: syncQueue) { [weak self] (data: [JSONData]) -> Promise<()> in
            guard let selfObj = self else {
                throw DBLoggingError.sessionDeallocated
            }
            
            guard let sendingEvents = selfObj.eventSender?.sendEventsToServer(data: data) else {
                throw DBLoggingError.noEventSender
            }
            
            return sendingEvents.recover { err -> Promise<()> in
                registerLogger.warning("Failed to send events to server")
                return Promise<()>(error: DBLoggingError.failedToSendEventsToServer)
            }
        }.then(on: syncQueue) { () -> () in //on success, delete logs from db
            let realm = try DBLoggingBackend.makeRealm()
            let objects = realm.objects(DBEventItem.self).filter("isSending = true")
            try realm.write {
                realm.delete(objects)
            }
            self.isSendingEvents = false
            registerCallbackQueue.async { [weak self] in
                self?._onEventsSent?()
            }
            return ()
        }
    }
}
