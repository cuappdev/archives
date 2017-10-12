import Foundation
import Alamofire
import PromiseKit
import SwiftyJSON
import RealmSwift

protocol EventSender: class {
    func sendEventsToServer(data: [JSONData]) -> Promise<()>
}

enum RegisterSessionError: Error {
    case failedToCombineJsonData
}

func combineArrayOfEvents(data: [JSONData]) throws -> JSONData {
    let strings = data.flatMap {String.init(data: $0, encoding: .utf8)}
    guard let result = "[\(strings.joined(separator: ","))]".data(using: .utf8) else {
        throw RegisterSessionError.failedToCombineJsonData
    }
    return result
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
        let combinedData: JSONData
        do {
            combinedData = try combineArrayOfEvents(data: data)
        } catch let e {
            return Promise(error: e)
        }
        
        return Alamofire.upload(combinedData, to: apiUrl.appendingPathComponent("multiple"), method: .post)
            .validate()
            .responseJSON()
            .then { response in
                let _ = JSON(data)
                return Promise(value: ())
            }
    }
}
