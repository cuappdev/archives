import Foundation
import RealmSwift
import PromiseKit

class DBEventItem : Object {
    @objc dynamic var serializedLog: JSONData = Data()
    @objc dynamic var eventName: String = ""
}

class DBLoggingBackend {
    
    private var sendTimer: Timer?
    weak var eventSender: EventSender?
    
    init(eventSender: EventSender) {
        self.eventSender = eventSender
    }
    
    func makeRealm() -> Realm {
        let realmConfig = Realm.Configuration(
            fileURL: URL.init(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("register.realm")
        )
        let realm = try! Realm(configuration: realmConfig)
        return realm
    }
    
    func logEvent<T: Loggable>(event: T) -> Promise<()> {
        return Promise { fulfill, reject in
            let dbEvent = DBEventItem()
            dbEvent.serializedLog = try event.serializeJson()
            dbEvent.eventName = event.eventName
            
            let realm = self.makeRealm()
            try! realm.write {
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
