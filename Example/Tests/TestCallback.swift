//
//  TestCallback.swift
//  SwiftRegister_Tests
//
//  Created by Serge-Olivier Amega on 2/17/18.
//  Copyright © 2018 CocoaPods. All rights reserved.
//

import SwiftRegister
import Foundation
import XCTest

class TestCallback: XCTestCase {
    let session = RegisterSession.init(apiUrl: testApiUrl, secretKey: testAppSecret, logMode: RegisterSession.LogMode.regular, eventSendingTimeInterval: 0.0)
    
    func testEventsSentCallback() {
        let syncQueue = DispatchQueue.init(label: "testEventsSentCallback")
        var eventsGotSent: Bool = false
        
        let eventsSent = expectation(description: "events sent")
        session.onEventsSent = {
            syncQueue.async {
                eventsGotSent = true
                eventsSent.fulfill()
            }
        }
        
        let event = AlphaPayload(value: "hello").toEvent()
        session.logEvent(event: event)
        
        wait(for: [eventsSent], timeout: 5)
        XCTAssert(eventsGotSent)
    }
}
