import Foundation
import PromiseKit
import Log

/**
 * Promise.then seems to confuse the compiler sometimes when
 * the function passed in is (T) throws -> U, and not (T) throws -> Promise<U>.
 */
public extension Promise {
    public func next<U>(execute: @escaping (T) throws -> U) -> Promise<U> {
        return self.then(execute: execute)
    }
}

let registerLogger: Logger = {
    //Init logger
    let formatter = Log.Formatter("[Register - %@] : %@", [.level, .message])
    return Logger.init(formatter: formatter, theme: nil, minLevel: .warning)
}()

public enum LoggingLevel {
    case debug, regular
}

/**
 * This function should only be called before using anything else from this library
 */
public func registerLoggerSetLevel(level: LoggingLevel) {
    switch level {
    case .debug:
        registerLogger.minLevel = .debug
    case .regular:
        registerLogger.minLevel = .warning
    }
}
