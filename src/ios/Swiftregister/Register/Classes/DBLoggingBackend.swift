import Foundation
import RealmSwift
import PromiseKit

class DBEventItem : Object {
    @objc dynamic var serializedLog: JSONData = Data()
    @objc dynamic var eventName: String = ""
}

enum DBLoggingError: Error {
    case realmFailedToCreate(reason: String), sessionDeallocated, noEventSender
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
            let dbEvent = DBEventItem()
            dbEvent.serializedLog = try event.serializeJson()
            dbEvent.eventName = event.eventName
            
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
        let sendingPromise = Promise<[JSONData]> { fulfill, reject in
            let realm = try DBLoggingBackend.makeRealm()
            let logs = Array(realm.objects(DBEventItem.self))
            let data = logs.map {$0.serializedLog}
            fulfill(data)
            }.then { [weak self] (data: [JSONData]) -> Promise<()> in
                guard let selfObj = self else {
                    throw DBLoggingError.sessionDeallocated
                }
                
                guard let result = selfObj.eventSender?.sendEventsToServer(data: data) else {
                    throw DBLoggingError.noEventSender
                }
                
                return result
            }.catch { _ in
                registerLogger.warning("Failed to send events to server")
        }
        
        return when(fulfilled: sendingPromise).next { (_:()) -> () in //on success, delete logs from db
            let realm = try DBLoggingBackend.makeRealm()
            
            try realm.write {
                realm.delete(realm.objects(DBEventItem.self))
            }
            return ()
        }.catch { _ in
            registerLogger.warning("Failed to delete events from database")
        }
    }
}
