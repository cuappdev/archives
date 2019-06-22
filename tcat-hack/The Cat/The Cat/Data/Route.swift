//
//  Route.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import Foundation

class Route: NSObject {
    let id: Int
    var schedule: [[RouteStop]] = []
    var stops: Set<String> = Set<String>()
    
    init(id: Int) {
        self.id = id
    }
}
