import Foundation
import PromiseKit

/**
 * This takes care of logging events. Create a new RegisterSession with a
 * loggingUrl and log events by calling logEvent
 */
public class RegisterSession {
    public enum LogMode {
        case debug, regular, errorOnly
    }
    
    let eventSender: EventSender
    let dbBackend: DBLoggingBackend
    
    /**
     * api url should be the url path including /api/
     * for example: http://localhost:5000/api/
     */
    public init(apiUrl: URL, secretKey: String, logMode: LogMode = .regular) {
        self.eventSender = MainEventSender(apiUrl: apiUrl, secretKey: secretKey)
        self.dbBackend = DBLoggingBackend(eventSender: self.eventSender)
    }
    
    public func logEvent<T>(event: Event<T>) -> Promise<()> {
        return dbBackend.logEvent(event: event)
    }
}
