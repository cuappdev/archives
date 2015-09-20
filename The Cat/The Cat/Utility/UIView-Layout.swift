//
//  UIView-Layout.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

extension UIView {
    
    var bottomEdge: CGFloat {
        return frame.origin.y + frame.height
    }
    
    var rightEdge: CGFloat {
        return frame.origin.x + frame.width
    }
    
    func setWidth(width: CGFloat) {
        frame.size = CGSize(width: width, height: frame.height)
    }
    
    func setHeight(height: CGFloat) {
        frame.size = CGSize(width: frame.width, height: height)
    }
}
