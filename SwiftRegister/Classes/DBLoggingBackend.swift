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

//TODO print errors if logging fails (in case user doesn't catch promises)
//TODO need to revamp the scheduled uploading system
// - background uploading
// - possibly use something besides NSTimer to reduce energy consumption (like gcd maybe)
// - If we use NSTimer, should we use a run loop besides RunLoop.main?
//TODO need delegate functions to notify when events are sent to the server
//TODO timestamp ids for logs to avoid doubles
class DBLoggingBackend {
    
    private var sendTimer: Timer?
    weak var eventSender: EventSender?
    let syncQueue: DispatchQueue
    let timerInterval: TimeInterval
    
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
            
            scheduleTimer(interval: timerInterval)

            fulfill(())
        }
    }
    
    func scheduleTimer(interval: TimeInterval) {
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
    
    @discardableResult
    func sendAllEvents() -> Promise<()> {
        return Promise(value: ())
        .then(on: syncQueue) { () -> [JSONData] in
            //synchronously get events from db and mark each event with isSending = true
            let realm = try DBLoggingBackend.makeRealm()
            let logs = Array(realm.objects(DBEventItem.self))
            try realm.write {
                logs.forEach {$0.isSending = true}
            }
            let data = logs.map {$0.serializedLog}
            return data
        }.then { [weak self] (data: [JSONData]) -> Promise<()> in
            guard let selfObj = self else {
                throw DBLoggingError.sessionDeallocated
            }
            
            guard let sendingEvents = selfObj.eventSender?.sendEventsToServer(data: data) else {
                throw DBLoggingError.noEventSender
            }
            
            sendingEvents.catch {
                registerLogger.warning("Failed to send events to server")
            }
            
            sendingEvents.recover { err -> Promise<()> in
                registerLogger.warning("Failed to send events to server")
                return Promise<()>(error: DBLoggingError.failedToSendEventsToServer)
            }
            
            return sendingEvents
        }.next { //on success, delete logs from db
            let realm = try DBLoggingBackend.makeRealm()
            let objects = realm.objects(DBEventItem.self).filter("isSending = true")
            try realm.write {
                realm.delete(objects)
            }
            return ()
        }
    }
}
