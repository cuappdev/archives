//
//  Macros.swift
//  BarstoolSports
//
//  Created by Eric Appel on 9/15/15.
//  Copyright (c) 2015 Eric Appel. All rights reserved.
//

import Foundation

func async(block: dispatch_block_t) {
    dispatch_async(dispatch_get_main_queue(), block)
}

func dispatchAfter(delay: Double, block: () -> Void) {
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, Int64(delay * Double(NSEC_PER_SEC))), dispatch_get_main_queue()) { () -> Void in
        block()
    }
}
