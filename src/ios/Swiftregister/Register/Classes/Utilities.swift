import Foundation
import PromiseKit

/**
 * Promise.then seems to confuse the compiler sometimes when
 * the function passed in is (T) throws -> U, and not (T) throws -> Promise<U>.
 */
public extension Promise {
    public func next<U>(execute: @escaping (T) throws -> U) -> Promise<U> {
        return self.then(execute: execute)
    }
}
