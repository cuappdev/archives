@testable import SwiftRegister
import Foundation
import XCTest

class TestEventSending: XCTestCase {
    let eventSender = MainEventSender(apiUrl: testApiUrl, secretKey: testAppSecret)
    
    func testEventSending() {
        let events = [
            CharliePayload(field1: "asdf", field2: 10),
            CharliePayload(field1: "zxcv", field2: 20),
        ].map(Event.init).map(TimestampedEvent.init)
        
        let eventData: [JSONData]
        do {
            eventData = try events.map({try $0.serializeJson()})
        } catch let error {
            XCTFail(error.localizedDescription)
            return
        }
        
        let serverReached = expectation(description: "server reached")
        var success = false
        
        eventSender.sendEventsToServer(data: eventData).then { () -> () in
            success = true
            serverReached.fulfill()
        }.catch { error -> () in
            print("server not reached")
            XCTFail(error.localizedDescription)
        }
        
        wait(for: [serverReached], timeout: 2)
        XCTAssert(success)
    }
}
