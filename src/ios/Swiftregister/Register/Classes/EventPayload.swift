import Foundation

protocol A {
    static var s: String {get}
}

/**
 * Any class/struct that implements this protocol is loggable.
 * Make sure that the type of the payload, T, is concrete
 */
public protocol Loggable: Codable {
    /**T must be a concrete type*/
    associatedtype T: Codable
    var eventName: String {get}
    var payload: T {get}
}

/**Use JSONData for serialized JSON*/
public typealias JSONData = Data

extension Loggable {
    public func serializeJson() throws -> JSONData {
        return try JSONEncoder().encode(self)
    }
}

