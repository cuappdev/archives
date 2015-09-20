//
//  Globals.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

enum ActiveSearchField {
    case Start
    case End
}

var activeSearchField: ActiveSearchField = .Start

let kStatusBarHeight: CGFloat = 20

typealias routeOption = (route: Route, stops: [RouteStop])
