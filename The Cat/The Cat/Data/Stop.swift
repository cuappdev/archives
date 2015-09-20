//
//  Stop.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import MapKit

enum AnnotationViewType: String {
    case Pin = "pin"
    case Selected = "selected"
    case Start = "start"
    case End = "end"
    case Intermediate = "intermediate"
}

class Stop: NSObject, MKAnnotation {
    let name: String
    let coordinate: CLLocationCoordinate2D
    
    var viewType: AnnotationViewType?
    
    init(name: String, latitude: Double, longitude: Double) {
        self.name = name
        self.coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)

    }
    
    convenience init?(json: JSON) {
        guard let name = json["Name"].string else { return nil }
        
        let lat = json["Latitude"].double
        let lon = json["Longitude"].double
        guard lat != nil && lon != nil else { return nil }
        
        self.init(name: name, latitude: lat!, longitude: lon!)
    }
    
    var title: String? {
        return name
    }
    
}

func stopsEquiv(a: String, b: String) -> Bool {
    let a = a.lowercaseString
    let b = b.lowercaseString
    
    if a == b { return true }
    if a.containsString(b) { return true }
    if b.containsString(a) { return true }
    return false
}