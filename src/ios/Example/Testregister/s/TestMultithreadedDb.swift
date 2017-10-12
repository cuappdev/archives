import Foundation
import XCTest
import PromiseKit
import SwiftyJSON
@testable import SwiftRegister

class TestEventSender: EventSender {
    let expectedEventsSentExpectation: XCTestExpectation
    let expectedNumberOfEvents: Int
    var sentEvents: [JSON] = []
    let syncQueue = DispatchQueue(label: "register_test.test_event_sender")
    
    init(expectedNumberOfEvents: Int, expectedEventsSentExpectation: XCTestExpectation) {
        self.expectedNumberOfEvents = expectedNumberOfEvents
        self.expectedEventsSentExpectation = expectedEventsSentExpectation
    }
    
    func sendEventsToServer(data: [JSONData]) -> Promise<()> {
        return syncQueue.promise {
            for dataElem in data {
                let json = JSON(dataElem)
                self.sentEvents.append(json)
            }
            if self.expectedNumberOfEvents == self.sentEvents.count {
                self.expectedEventsSentExpectation.fulfill()
            }
        }
    }
}

class DBMultithreadedLoggingTestCase: XCTestCase {
    
    static let numberOfEvents = 100
    var events = (0..<numberOfEvents).map {
        AlphaEvent(payload: "payload_\($0)")
    }
    let syncQueue = DispatchQueue(label: "register_test.db_multithreading_logging")
    
    func getEvent() -> AlphaEvent? {
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
        syncQueue.sync {
            for event in events {
                let foundEvent = eventSender.sentEvents.first { json in
                    json["eventName"].string == event.eventName &&
                    json["payload"].string == event.payload
                }
                XCTAssert(foundEvent != nil)
            }
        }
        
        //make sure db has no more events
        let realm = try! DBLoggingBackend.makeRealm()
        XCTAssert(realm.objects(DBEventItem.self).count == 0)
    }
}

