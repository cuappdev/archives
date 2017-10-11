import Foundation
import RealmSwift
import PromiseKit

class DBEventItem : Object {
    @objc dynamic var serializedLog: JSONData = Data()
    @objc dynamic var eventName: String = ""
}

enum DBLoggingError: Error {
    case realmFailedToCreate(reason: String)
}

class DBLoggingBackend {
    
    private var sendTimer: Timer?
    weak var eventSender: EventSender?
    
    init(eventSender: EventSender) {
        self.eventSender = eventSender
    }
    
    func makeRealm() throws -> Realm {
        let realmConfig = Realm.Configuration(
            fileURL: URL.init(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("register.realm")
        )
        do {
            return try Realm(configuration: realmConfig)
        } catch let e {
            throw DBLoggingError.realmFailedToCreate(reason: e.localizedDescription)
        }
    }
    
    func logEvent<T: Loggable>(event: T) -> Promise<()> {
        return Promise { fulfill, reject in
            let dbEvent = DBEventItem()
            dbEvent.serializedLog = try event.serializeJson()
            dbEvent.eventName = event.eventName
            
            let realm = try self.makeRealm()
            
            try realm.write {
                realm.add(dbEvent)
            }
            
            //set up the sending timer
            if self.sendTimer == nil {
                self.sendTimer = Timer.init(timeInterval: 10, repeats: true, block: {[weak self] _ in
                    self?.sendAllEvents()
                })
            }
            fulfill(())
        }
    }
    
    func sendAllEvents() {
        print("sendAllEvents unimplemented!")
    }
}
