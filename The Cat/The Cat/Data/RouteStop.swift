//
//  RouteStop.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class RouteStop: NSObject {
    let stopName: String
    let date: NSDate
    var time: String {
        return dateToTime(date)
    }
    let day: String
    let route: Int
    let instance: Int
    
    override var description: String {
        return "\(route) [\(time)] - \(stopName)"
    }
    
    
    init(stopName: String, time: NSDate, day: String, route: Int, instance: Int) {
        self.stopName = stopName
        self.date = time
        self.day = day
        self.route = route
        self.instance = instance
    }
    
    convenience init?(json: JSON) {
        guard let name = json["Stop"].string else { return nil }
        guard let time = json["Time"].string else { return nil }
        guard let date = timeToDate(time) else { return nil }
        guard let day = json["Day"].string else { return nil }
        guard let route = json["Route"].int else { return nil }
        guard let instance = json["RouteInstance"].int else { return nil }

        self.init(stopName: name, time: date, day: day, route: route, instance: instance)
    }
    
    
}

func timeToDate(time: String) -> NSDate? {
    let dateFormatter = NSDateFormatter()
    dateFormatter.dateFormat = "h:mma"
    
    guard let date = dateFormatter.dateFromString(time) else { return nil }
    
    return date
}

func dateToTime(date: NSDate) -> String {
    let dateFormatter = NSDateFormatter()
    dateFormatter.dateFormat = "h:mma"
    
    let str = dateFormatter.stringFromDate(date)
    
    return str
}
