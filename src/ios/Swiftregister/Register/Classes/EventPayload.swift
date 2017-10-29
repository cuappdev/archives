import Foundation

public protocol Payload: Codable {
    static var eventName: String {get}
}

/**Use JSONData for serialized JSON*/
public typealias JSONData = Data

public enum EventError: Error {
    case wrongEventName
}

public class Event<TPayload: Payload>: Codable {
    public let payload: TPayload
    public var eventName: String {return TPayload.eventName}
    
    init(payload: TPayload) {
        self.payload = payload
    }
    
    public required init(from decoder: Decoder) throws {
        let values = try decoder.container(keyedBy: CodingKeys.self)
        self.payload = try values.decode(TPayload.self, forKey: .payload)
        let decodedEventName = try values.decode(String.self, forKey: .eventName)
        if decodedEventName != eventName {
            throw EventError.wrongEventName
        }
    }
    
    public func encode(to encoder: Encoder) throws {
        var values = encoder.container(keyedBy: CodingKeys.self)
        try values.encode(self.payload, forKey: .payload)
        try values.encode(self.eventName, forKey: .eventName)
    }
    
    enum CodingKeys: String, CodingKey {
        case timestamp, payload, eventName
    }
    
    public func serializeJson() throws -> JSONData {
        return try JSONEncoder().encode(self)
    }
}

public class TimestampedEvent<TPayload: Payload>: Event<TPayload> {
    public let timestamp: Date
    
    init(event: Event<TPayload>) {
        self.timestamp = Date()
        super.init(payload: event.payload)
    }
    
    init(event: Event<TPayload>, timestamp: Date) {
        self.timestamp = timestamp
        super.init(payload: event.payload)
    }
    
    public required init(from decoder: Decoder) throws {
        let values = try decoder.container(keyedBy: CodingKeys.self)
        self.timestamp = try values.decode(Date.self, forKey: .timestamp)
        try super.init(from: decoder)
    }
    
    public override func encode(to encoder: Encoder) throws {
        try super.encode(to: encoder)
        var values = encoder.container(keyedBy: CodingKeys.self)
        try values.encode(self.timestamp, forKey: .timestamp)
    }
}
