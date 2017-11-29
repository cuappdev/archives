import Foundation
import XCTest
import SwiftyJSON
@testable import SwiftRegister

class TestTimestampsAreGMT: XCTestCase {
    func testTimestampGMT() {
        let event = Event(payload: AlphaPayload(value: "hello"))
        let timestampedEvent = TimestampedEvent(event: event)
        let jsonData = try! timestampedEvent.serializeJson()
        let json = JSON(jsonData)
        guard let timestampString = json["timestamp"].string else {
            XCTFail("json doesn't contain timestamp")
            return
        }
        guard timestampString.range(of: "GMT") != nil else {
            XCTFail("timestamp not in GMT")
            return
        }
    }
}
