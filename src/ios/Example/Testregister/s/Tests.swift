import UIKit
import XCTest
import SwiftRegister

struct AlphaPayload: Payload {
    static let eventName: String = "alpha"
    let value: String
}

struct BravoPayload: Payload {
    static let eventName: String = "bravo"
    let kind: String
    let magnitude: Float
}
