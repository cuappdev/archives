import UIKit
import XCTest
import SwiftRegister

struct AlphaEvent: Loggable {
    let eventName: String = "alpha"
    let payload: String
}

class Tests: XCTestCase {
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testExample() {
    }
    
    func testEncode() {
        let alpha = AlphaEvent(payload: "ok")
        let data = alpha.toEncodedEvent()
        print(String(data: data, encoding: .utf8))
    }
    
}
