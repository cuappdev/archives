import PromiseKit
import Foundation
import SwiftyJSON

protocol EventSender: class {
    func sendEventsToServer(data: [JSONData]) -> Promise<()>
}

enum EventSenderError: Error {
    case failedToCombineJsonData
    case serverError(String?)
}

func combineArrayOfEvents(data: [JSONData]) throws -> JSONData {
    let arrayOfJsonEvents: [JSON] = try data.flatMap {try JSON(data: $0)}
    guard let result = try? JSON(["events": JSON(arrayOfJsonEvents)]).rawData() else {
        throw EventSenderError.failedToCombineJsonData
    }
    return result
}

class MainEventSender: EventSender {
    
    let apiUrl: URL
    let secretKey: String
    
    /**
     * Initializes the event sender with the given api url
     * api url should be the url path including /api/
     * for example: http://localhost:5000/api/
     */
    init(apiUrl: URL, secretKey: String) {
        self.apiUrl = apiUrl
        self.secretKey = secretKey
    }
    
    /**Tries to send events to the server*/
    public func sendEventsToServer(data: [JSONData]) -> Promise<()> {
        let combinedData: JSONData
        do {
            combinedData = try combineArrayOfEvents(data: data)
        } catch let e {
            return Promise(error: e)
        }
        
        let urlToSend = apiUrl.appendingPathComponent("events/create/")
        String(data: combinedData, encoding: .utf8).map {registerLogger.debug("sending data to \(urlToSend)\n\($0)")}
        
        let headers = [
            "Authorization" : "Bearer \(self.secretKey)",
            "Content-Type" : "application/json"
        ]
        return Alamofire.upload(combinedData,
                                to: urlToSend,
                                method: .post, headers: headers)
            .validate()
            .responseJSON()
            .then { response in
                let json = JSON(response)
                json.rawString().map{ registerLogger.debug("received from server:\n\($0)") }
                if json["success"].bool != true {
                    return Promise(error: EventSenderError.serverError(json["data"]["errors"].string))
                } else {
                    return Promise(value: ())
                }
        }
    }
}
