//
//  Network.swift
//  big-red-shuttle
//
//  Created by Austin Astorga on 10/19/16.
//  Copyright © 2016 cuappdev. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON

class API {
    
    static let sharedAPI = API()
    
    /// registers a user to log location using an authentication key
    func registerUserToLogLocation(uid: String, key: String) {
        
    }
    
    /// logs the location of the shuttle
    func logLocation(uid: String, longitude: String, latitude: String) {
        
    }
    
    /// fetches the last logged location of the shuttle
    func getLocation(uid: String, completion: (String, String) -> ()) {
        
    }
}


public func getStops() ->  [Stop] {
    let stopJsonString = "https://raw.githubusercontent.com/cuappdev/big-red-shuttle-stack/master/big-red-shuttle.json"
    var stops = [Stop]()
    if let url = URL(string: stopJsonString) {
        if let data = try? Data(contentsOf: url) {
            let json = JSON(data: data)
            for stop in json["stops"].arrayValue {
                var dayArray = [Days]()
                let name = stop["name"].stringValue
                let lat = stop["lat"].floatValue
                let long = stop["long"].floatValue
                let days = stop["days"].arrayObject!
                
                for day in days {
                    dayArray.append(Days(rawValue: day as! String)!)
                }
                
                let timeStrings = stop["times"].arrayObject! as! [String]
                var times:[Time] = []
                for tStr in timeStrings {
                    times.append(getTime(time: tStr))
                }
                times = times.sorted(by: timeCompare)
                stops.append(Stop(name: name, lat: lat, long: long, days: dayArray, times: times))
  
            }
        }
    }
    return stops

}

/* Creates time from JSON string
 * Time string must have format:
 * H:mm a
 */
public func getTime(time: String) -> Time{
    var hourArr = time.components(separatedBy: ":") //["h","mm a"]
    let minArr = hourArr[1].components(separatedBy: " ") //["mm","a"]
    let timeArr = [hourArr[0]] + minArr //["h","mm","a"]
    
    let minute = Int(timeArr[1])!
    
    let hour12 = Int(hourArr[0])!
    
    var hour = 0
    let aa = timeArr[2].lowercased()
    if(aa=="am" && hour12 == 12){ //12:xx am = 0:xx
        hour = 0
    }else if(aa=="pm" && hour12 != 12){ //12:xx pm = 12:xx
        hour = hour12 + 12 //h:xx pm = (h+12):xx
    }else{
        hour = hour12
    }
    
    return Time(hour: hour, minute: minute)
}
