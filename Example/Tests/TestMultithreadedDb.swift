import Foundation
import XCTest
import PromiseKit
import SwiftyJSON
@testable import SwiftRegister

class TestEventSender: EventSender {
    let expectedEventsSentExpectation: XCTestExpectation?
    let expectedNumberOfEvents: Int
    var sentEvents: [JSON] = []
    let syncQueue = DispatchQueue(label: "register_test.test_event_sender")
    let sendDelayTime: TimeInterval
    
    init(expectedNumberOfEvents: Int, expectedEventsSentExpectation: XCTestExpectation? = nil, sendDelayTime: TimeInterval = 0.0) {
        self.expectedNumberOfEvents = expectedNumberOfEvents
        self.expectedEventsSentExpectation = expectedEventsSentExpectation
        self.sendDelayTime = sendDelayTime
    }
    
    func sendEventsToServer(data: [JSONData]) -> Promise<()> {
        return after(seconds: sendDelayTime).then(on: syncQueue) { () -> () in
            for dataElem in data {
                let json = JSON(dataElem)
                self.sentEvents.append(json)
            }
            if self.expectedNumberOfEvents == self.sentEvents.count {
                self.expectedEventsSentExpectation?.fulfill()
            }
        }
    }
}

class DBMultithreadedLoggingTestCase: XCTestCase {
    
    static let numberOfEvents = 100
    var events = (0..<numberOfEvents).map {
        AlphaPayload(value: "payload_\($0)").toEvent()
    }
    let syncQueue = DispatchQueue(label: "register_test.db_multithreading_logging")
    
    func getEvent() -> Event<AlphaPayload>? {
        return syncQueue.sync { events.popLast() }
    }
    
    override func setUp() {
        let realm = try! DBLoggingBackend.makeRealm()
        try! realm.write {
            realm.deleteAll()
        }
    }
    
    func testMultithreadedLogging() {
        let sentAllEvents = expectation(description: "sent all events")
        let logClientQueue = DispatchQueue.init(label: "register_test.db_multithreading_client", attributes: DispatchQueue.Attributes.concurrent)
        
        let eventSender = TestEventSender(expectedNumberOfEvents: events.count, expectedEventsSentExpectation: sentAllEvents)
        let backend = DBLoggingBackend(eventSender: eventSender, timerInterval: 3)
        
        (0..<10).forEach { _ in
            logClientQueue.asyncAfter(deadline: .now() + 0.2) { [weak self] in
                while let event = self?.getEvent() {
                    backend.logEvent(event: event)
                }
            }
        }
        
        wait(for: [sentAllEvents], timeout: 6)
        XCTAssert(eventSender.sentEvents.count == DBMultithreadedLoggingTestCase.numberOfEvents)
        
        //make sure all events were sent
        var eventNilFlag = false
        syncQueue.sync {
            for event in events {
                let foundEvent = eventSender.sentEvents.first { json in
                    json["eventName"].string == event.eventName &&
                    json["payload"].string == event.payload.value
                }
                if foundEvent == nil {
                    eventNilFlag = true
                    break
                }
            }
        }
        XCTAssert(eventNilFlag == false)
        
        //make sure db has no more events
        let realm = try! DBLoggingBackend.makeRealm()
        XCTAssert(realm.objects(DBEventItem.self).count == 0)
    }
    
    func testSubsequentEventSending() {
        let events = [
            "first", "second", "third", "fourth"
        ].map { AlphaPayload(value: $0).toEvent() }
        let eventsSentExpectation = expectation(description: "events sent")
        
        let eventSender = TestEventSender(expectedNumberOfEvents: events.count, expectedEventsSentExpectation: eventsSentExpectation, sendDelayTime: 1.0)
        let backend = DBLoggingBackend(eventSender: eventSender, timerInterval: 0.0)
        
        for event in events {
            backend.logEvent(event: event)
        }
        
        wait(for: [eventsSentExpectation], timeout: 3.0)
        XCTAssert(eventSender.sentEvents.count == events.count)
    }
}

