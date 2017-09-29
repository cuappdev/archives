import Foundation
import Alamofire
import PromiseKit
import SwiftyJSON

/**
 * This takes care of logging events. Create a new RegisterSession with a
 * loggingUrl and log events by calling logEvent
 */
class RegisterSession {
    let loggingUrl: URL
    
    init(loggingUrl: URL) {
        self.loggingUrl = loggingUrl
    }
    
    func logEvent<T: Loggable>(event: T) -> Promise<()> {
        let serializedEvent: Data
        do {
            serializedEvent = try event.serialize()
        } catch let e {
            return Promise<()>(error: e)
        }
        
        return Alamofire.upload(serializedEvent, to: loggingUrl, method: .post)
            .validate()
            .responseJSON()
            .then { data in
                let json = JSON(data)
                //TODO check json for errors
                return Promise(value: ())
        }
    }
}
