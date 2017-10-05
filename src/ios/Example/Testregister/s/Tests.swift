import UIKit
import XCTest
import SwiftRegister

struct AlphaEvent: Loggable {
    let eventName: String = "alpha"
    let payload: String
}

struct BravoEvent: Loggable {
    let eventName: String = "bravo"
    let payload: BravoPayload
}

struct BravoPayload: Codable {
    let kind: String
    let magnitude: Float
}
