import Foundation

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

extension Loggable {
    public func serialize() throws -> Data {
        return try JSONEncoder().encode(self)
    }
}
