//
//  EventSender.swift
//  SwiftRegister
//
//  Created by Serge-Olivier Amega on 11/15/17.
//

import PromiseKit
import Foundation
import SwiftyJSON

protocol EventSender: class {
    func sendEventsToServer(data: [JSONData]) -> Promise<()>
}

enum EventSenderError: Error {
    case failedToCombineJsonData
}

func combineArrayOfEvents(data: [JSONData]) throws -> JSONData {
    let strings = data.flatMap {String.init(data: $0, encoding: .utf8)}
    guard let result = "[\(strings.joined(separator: ","))]".data(using: .utf8) else {
        throw EventSenderError.failedToCombineJsonData
    }
    return result
}

class MainEventSender: EventSender {
    
    let apiUrl: URL
    
    init(apiUrl: URL) {
        self.apiUrl = apiUrl
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
