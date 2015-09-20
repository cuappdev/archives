//
//  Globals.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import CoreLocation

enum ActiveSearchField {
    case Start
    case End
}

var _activeSearchField: ActiveSearchField = .Start
var activeSearchField: ActiveSearchField {
get {
    return _activeSearchField
}
set(newValue) {
    _activeSearchField = newValue
    if newValue == .Start {
        startUnderline.hidden = false
        endUnderline.hidden = true
    } else {
        startUnderline.hidden = true
        endUnderline.hidden = false
    }
}
}

var startUnderline: UIView!
var endUnderline: UIView!


let kStatusBarHeight: CGFloat = 20

typealias routeOption = (route: Route, stops: [RouteStop])

let locationManager = CLLocationManager()

var stopsDict: [String:Stop] = [:]
