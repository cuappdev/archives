# SwiftRegister

## Installing

For now, you can install using CocoaPods by pointing CocoaPods to this repository.

```ruby
use_frameworks!
platform :ios, '11.0'

target 'MyApp' do
  pod 'SwiftRegister', :git=> 'https://github.com/cuappdev/register-client.git', :commit => 'master'
end
```

## Using SwiftRegister

### Getitng Started

First, register your app with the register server, and obtain the secret key for your app. Next, register your events with the server using the rest API (TODO rest api doc).

Now that your events are registered, create structs that subclass `Payload`. This includes a field that identifies the event type, and another field that contains the payload associated with each event. Next, create a register session.

```swift
struct UpvotePressPayload: Payload {
   static let eventName: String = "upvotePress"
   let buttonType: String
   let durationOfPress: Float
}

let session = RegisterSession(apiUrl: apiUrl, secretKey: secret)
```

The next snippet of code shows how you would submit an event. Events are written to disk and sent in batches.

```swift
@IBAction func upvoteReleased(upvoteButton: UpvoteButton) {
    let duration = upvoteButton.pressDuration
    let buttonType = upvoteButton.isBlue ? "blue" : "regular"
    let upvoteEvent = Event(payload:
        UpvotePressPayload(buttonType: buttonType, durationOfPress: duration))
    session.logEvent(event: upvoteEvent)
}
```

You can also execute some code after an event is successfully written to disk.

```swift
session.logEvent(event: upvoteEvent).next { () in
    print("event logged")
}
```

### Custom Keys

You can specify custom keys for your payload by creating a CodingKeys enum as follows:

```swift
struct UpvotePressPayload: Payload {
   static let eventName: String = "upvotePress"
   let buttonType: String
   let durationOfPress: Float

   private enum CodingKeys: String, CodingKey {
      case buttonType = "button_type"
      case durationOfPress = "duration_of_press"
   }
}
```

This works because the Payload protocol inherits from Swift.Codable. See more [here](https://developer.apple.com/documentation/swift/codable)

