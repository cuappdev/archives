import UIKit
import XCTest
import SwiftRegister

//let testAppSecret = "018c5653072942f43215be586c967ad82352b2c2"
//let testApiUrl = URL(string: "http://localhost:5000/api/")!

let testAppSecret = "984229841cb1f5a1aad41ff0227f2aa2ef7c7ed8"
let testApiUrl = URL(string: "http://52.54.98.130/api/")!

struct AlphaPayload: Payload {
    static let eventName: String = "alpha"
    let value: String
}

struct BravoPayload: Payload {
    static let eventName: String = "bravo"
    let kind: String
    let magnitude: Float
}

struct CharliePayload: Payload {
    static let eventName: String = "charlie"
    let field1: String
    let field2: Int
}

