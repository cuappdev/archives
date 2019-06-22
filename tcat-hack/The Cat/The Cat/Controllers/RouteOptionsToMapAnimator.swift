//
//  RouteOptionsToMapAnimator.swift
//  The Cat
//
//  Created by Eric Appel on 9/20/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class RouteOptionsToMapAnimator: NSObject, UIViewControllerAnimatedTransitioning {
    static let sharedAnimator = RouteOptionsToMapAnimator()
    
    func transitionDuration(transitionContext: UIViewControllerContextTransitioning?) -> NSTimeInterval {
        return 0.4
    }
    
    func animateTransition(transitionContext: UIViewControllerContextTransitioning) {
        let toViewController = transitionContext.viewControllerForKey(UITransitionContextToViewControllerKey) as! MainViewController
        let fromViewController = transitionContext.viewControllerForKey(UITransitionContextFromViewControllerKey) as! RouteOptionsViewController
        
        toViewController.view.frame.origin = CGPoint(x: -toViewController.view.frame.width, y: 0)
//        fromViewController.view.frame.origin = CGPointZero
        
        transitionContext.containerView()?.addSubview(toViewController.view)
        
        UIView.animateWithDuration(transitionDuration(transitionContext), animations: { () -> Void in
            toViewController.view.frame.origin = CGPointZero
//            fromViewController.view.frame.origin = CGPoint(x: fromViewController.view.frame.width, y: 0)
            }) { (_) -> Void in
                transitionContext.completeTransition(!transitionContext.transitionWasCancelled())
                toViewController.navigationController?.delegate = toViewController
        }
    }
    
}
