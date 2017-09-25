import SwiftyJSON

public func sayHi() -> String {
    return "Hello, World!"
}

public func helloJson() -> JSON {
    return JSON.init(parseJSON: "{\"hello\": \"world!\"}")
}
