import Foundation
import PromiseKit

let registerCallbackQueue = DispatchQueue(label: "register.callback_queue")

/**
 * This takes care of logging events. Create a new RegisterSession with a
 * loggingUrl and log events by calling logEvent.
 */
public class RegisterSession {
    public enum LogMode {
        case debug, regular, errorOnly
    }
    
    public var onEventsSent: (() -> ())?
    
    let eventSender: EventSender
    let dbBackend: DBLoggingBackend
    
    /**
     * api url should be the url path including /api/
     * for example: http://localhost:5000/api/
     */
    public init(apiUrl: URL, secretKey: String, logMode: LogMode = .regular, eventSendingTimeInterval: TimeInterval = 10.0) {
        self.eventSender = MainEventSender(apiUrl: apiUrl, secretKey: secretKey)
        self.dbBackend = DBLoggingBackend(eventSender: self.eventSender, timerInterval: eventSendingTimeInterval)
        self.dbBackend.onEventsSent = {
            registerCallbackQueue.async { [weak self] in self?.onEventsSent?() }
        }
    }
    
    /**
     * Log an event. thread safe.
     */
    @discardableResult
    public func logEvent<T>(event: Event<T>) -> Promise<()> {
        return dbBackend.logEvent(event: event)
    }
}
