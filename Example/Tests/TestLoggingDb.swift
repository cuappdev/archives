//
//  TestLoggingDb.swift
//  SwiftRegister_Tests
//
//  Created by Serge-Olivier Amega on 10/5/17.
//  Copyright © 2017 CocoaPods. All rights reserved.
//

import Foundation
import XCTest
import PromiseKit
import SwiftyJSON
@testable import SwiftRegister

class SessionTestCase: XCTestCase {
    let session: RegisterSession = RegisterSession(apiUrl: URL(string: "localhost")!)
    
    override func setUp() {
        let realm = session.dbBackend.makeRealm()
        try! realm.write {
            realm.deleteAll()
        }
    }
}

class TestLoggingDb: SessionTestCase {
    
    func testLogToDb() {
        let alpha = AlphaEvent(payload: "ok")
        let serialized = try! alpha.serializeJson()
        let promise = session.logEvent(event: alpha).next {
            let realm = self.session.dbBackend.makeRealm()
            let objs = realm.objects(DBEventItem.self)
            XCTAssertTrue(objs.contains {
                $0.eventName == alpha.eventName && $0.serializedLog == serialized
            }, "database should contain event")
        }
    }
    
    func testCombinedDbEventsValid() {
        let alpha = AlphaEvent(payload: "hello, world!")
        let bravo1 = BravoEvent(payload: BravoPayload(kind: "AKind", magnitude: 3.0))
        let bravo2 = BravoEvent(payload: BravoPayload(kind: "BKind", magnitude: 10.0))
        
        let finished = expectation(description: "test finished")
        
        let _ = when(resolved: [
            session.logEvent(event: alpha),
            session.logEvent(event: bravo1),
            session.logEvent(event: bravo2)
            ]).next { _ in
                let realm = self.session.dbBackend.makeRealm()
                let dataArray = Array(realm.objects(DBEventItem.self).map {$0.serializedLog})
                let jsonData = try! combineArrayOfEvents(data: dataArray)
                let json = JSON(jsonData)
                
                guard let jsonArr = json.array else {
                    XCTFail("expected an array")
                    return
                }
                
                let containsBravo1 = jsonArr.contains { json in
                    json["payload"]["magnitude"].float == bravo1.payload.magnitude &&
                    json["payload"]["kind"].string == bravo1.payload.kind &&
                    json["eventName"].string == bravo1.eventName
                }
                
                let containsBravo2 = jsonArr.contains { json in
                    json["payload"]["magnitude"].float == bravo2.payload.magnitude &&
                    json["payload"]["kind"].string == bravo2.payload.kind &&
                    json["eventName"].string == bravo2.eventName
                }
                
                let containsAlpha = jsonArr.contains { json in
                    json["payload"].string == alpha.payload &&
                    json["eventName"].string == alpha.eventName
                }
                
                XCTAssertTrue(containsBravo1)
                XCTAssertTrue(containsBravo2)
                XCTAssertTrue(containsAlpha)
                finished.fulfill()
        }
        
        wait(for: [finished], timeout: 10)
    }
    
}
