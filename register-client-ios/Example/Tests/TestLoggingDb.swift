import Foundation
import XCTest
import PromiseKit
import SwiftyJSON
import RealmSwift
@testable import SwiftRegister

//TODO use something besides XCTest because of its hard to debug NSExceptions
//TODO use AwaitKit to avoid wait.
class SessionTestCase: XCTestCase {
    let session: RegisterSession = RegisterSession(apiUrl: testApiUrl, secretKey: testAppSecret)
    
    override func setUp() {
        let realm = try! DBLoggingBackend.makeRealm()
        try! realm.write {
            realm.deleteAll()
        }
    }
}

class TestLoggingDb: SessionTestCase {
    
    func testLogToDb() {
        let alpha = AlphaPayload(value: "ok").toEvent()
        let done = expectation(description: "finished promise")
        var realmContainsEvents = false
        let _ = session.logEvent(event: alpha).next { () in
            let realm = try! DBLoggingBackend.makeRealm()
            let objs = realm.objects(DBEventItem.self)
            realmContainsEvents = objs.contains {
                let timestampedTestEvent = TimestampedEvent(event: alpha, timestamp: $0.timestamp)
                let serialized = try! timestampedTestEvent.serializeJson()
                return $0.eventName == alpha.eventName && $0.serializedLog == serialized
            }
            done.fulfill()
        }
        
        wait(for: [done], timeout: 1)
        XCTAssertTrue(realmContainsEvents, "database should contain event")
    }
    
    func testCombinedDbEventsValid() {
        let alpha = AlphaPayload(value: "hello, world!").toEvent()
        let bravo1 = BravoPayload(kind: "AKind", magnitude: 3.0).toEvent()
        let bravo2 = BravoPayload(kind: "BKind", magnitude: 10.0).toEvent()
        var (containsBravo1, containsBravo2, containsAlpha) = (false, false, false)
        
        let finished = expectation(description: "test finished")
        
        let _ = when(resolved: [
            session.logEvent(event: alpha),
            session.logEvent(event: bravo1),
            session.logEvent(event: bravo2)
            ]).next { _ in
                let realm = try! DBLoggingBackend.makeRealm()
                let dataArray = Array(realm.objects(DBEventItem.self).map {$0.serializedLog})
                let jsonData = try! combineArrayOfEvents(data: dataArray)
                let json = JSON(jsonData)
                
                guard let jsonArr = json["events"].array else {
                    XCTFail("expected an array")
                    return
                }
                
                containsBravo1 = jsonArr.contains { json in
                    json["payload"]["magnitude"].float == bravo1.payload.magnitude &&
                    json["payload"]["kind"].string == bravo1.payload.kind &&
                    json["event_type"].string == bravo1.eventName
                }
                
                containsBravo2 = jsonArr.contains { json in
                    json["payload"]["magnitude"].float == bravo2.payload.magnitude &&
                    json["payload"]["kind"].string == bravo2.payload.kind &&
                    json["event_type"].string == bravo2.eventName
                }
                
                containsAlpha = jsonArr.contains { json in
                    json["payload"]["value"].string == alpha.payload.value &&
                    json["event_type"].string == alpha.eventName
                }
                
                finished.fulfill()
        }
        
        wait(for: [finished], timeout: 10)
        XCTAssertTrue(containsBravo1)
        XCTAssertTrue(containsBravo2)
        XCTAssertTrue(containsAlpha)
    }
    
}