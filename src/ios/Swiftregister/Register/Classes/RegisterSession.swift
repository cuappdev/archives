import Foundation
import Alamofire
import PromiseKit
import SwiftyJSON
import RealmSwift

protocol EventSender: class {
    func sendEventsToServer(data: [JSONData]) -> Promise<()>
}

//TODO move this to somewhere more appropriate
//TODO make json Data safely typed
func combineArrayOfEvents(data: [JSONData]) -> JSONData {
    //in the future, this function should accept a JSONData type, which means this force unwrap will be safe
    let strings = data.map({String.init(data: $0, encoding: .utf8)!})
    return "[\(strings.joined(separator: ","))]".data(using: .utf8)!
}

/**
 * This takes care of logging events. Create a new RegisterSession with a
 * loggingUrl and log events by calling logEvent
 */
public class RegisterSession: EventSender {
    let apiUrl: URL
    var _dbBackend: DBLoggingBackend?
    var dbBackend: DBLoggingBackend {
        if _dbBackend == nil {
            _dbBackend = DBLoggingBackend(eventSender: self)
        }
        return _dbBackend!
    }
    
    public init(apiUrl: URL) {
        self.apiUrl = apiUrl
    }
    
    func logEventToServer<T: Loggable>(event: T) -> Promise<()> {
        let serializedEvent: Data
        do {
            serializedEvent = try event.serializeJson()
        } catch let e {
            return Promise<()>(error: e)
        }
        
        return Alamofire.upload(serializedEvent, to: apiUrl.appendingPathComponent("single"), method: .post)
            .validate()
            .responseJSON()
            .then { data in
                let _ = JSON(data)
                //TODO check json for errors
                return Promise(value: ())
            }
    }
    
    public func logEvent<T: Loggable>(event: T) -> Promise<()> {
        return dbBackend.logEvent(event: event)
    }
    
    /**Tries to send events to the server*/
    public func sendEventsToServer(data: [JSONData]) -> Promise<()> {
        let data = combineArrayOfEvents(data: data)
        return Alamofire.upload(data, to: apiUrl.appendingPathComponent("multiple"), method: .post)
            .validate()
            .responseJSON()
            .then { response in
                let _ = JSON(data)
                return Promise(value: ())
            }
    }
}
