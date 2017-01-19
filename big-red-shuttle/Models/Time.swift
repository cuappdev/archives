//
//  Time.swift
//  big-red-shuttle
//
//  Created by Monica Ong on 10/26/16.
//  Copyright © 2016 cuappdev. All rights reserved.
//

import Foundation

// Stores time using 24-hour system
public class Time: NSObject {
    public var hour: Int // in 24 hours
    public var minute: Int
    public var day: Int
    
    public var shortDescription: String {
        let civilianHour = hour == 0 ? 12 : hour % 12
        let displayMinute = minute < 10 ? "0\(minute)" : "\(minute)"
        let ampm = hour < 12 ? "am" : "pm"
        
        return "\(civilianHour):\(displayMinute) \(ampm)"
    }
    
    override public var description: String {
        let dayString = Days.fromNumber(num: day == 1 ? 7 : day - 1)!.rawValue
        return "\(shortDescription) on \(dayString) night"
    }
    
    public convenience init(day: Int, time: String) {
        let (hour, minute) = getTime(time: time)
        self.init(day: day, hour: hour, minute: minute)
    }
    
    public init(hour: Int, minute: Int, day: Int){
        self.hour = hour
        self.minute = minute
        self.day = day
    }
    
    public init(day: Int, hour: Int, minute: Int){
        self.day = day
        self.hour = hour
        self.minute = minute
    }
    
    public func isEarlier(than time: Time) -> Bool {
        if day < time.day || (day == 7 && time.day == 1) {
            return true
        } else if day > time.day {
            return false
        } else if hour > time.hour {
            return false
        } else if hour < time.hour {
            return true
        } else{
            return minute <= time.minute
        }
    }
    
    public func atMost24HoursLater(than time: Time) -> Bool {
        if day == time.day {
            if hour > time.hour {
                return true
            } else if hour == time.hour {
                return minute >= time.minute
            }
        } else if time.dayBefore(time: self) {
            if hour < time.hour {
                return true
            } else if hour == time.hour {
                return minute <= time.minute
            }
        }
        return false
    }
    
    public func atMost12HoursLater(than time: Time) -> Bool {
        if day == time.day {
            if hour == time.hour {
                return minute >= time.minute
            } else if hour < time.hour + 12 {
                return true
            }
        } else if time.dayBefore(time: self) {
            let hourDiff = 24 - hour + time.hour
            if hourDiff == 12 {
                return minute <= time.minute
            } else if hourDiff < 12 {
                return true
            }
        }
        return false
    }
    
    public func sameDay(asTime time: Time) -> Bool {
        return day == time.day
    }
    
    public func dayBefore(time: Time) -> Bool {
        return time.day == 1 ? day == 7 : time.day - 1 == day
    }
}
