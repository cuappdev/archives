//
//  RouteOptionsAnimator.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class RouteOptionsAnimator: NSObject, UIViewControllerAnimatedTransitioning {
    static let sharedAnimator = RouteOptionsAnimator()
    
    func transitionDuration(transitionContext: UIViewControllerContextTransitioning?) -> NSTimeInterval {
        return 0.4
    }
    
    func animateTransition(transitionContext: UIViewControllerContextTransitioning) {
        let toViewController = transitionContext.viewControllerForKey(UITransitionContextToViewControllerKey) as! RouteOptionsViewController
//        let fromViewController = transitionContext.viewControllerForKey(UITransitionContextFromViewControllerKey) as! RouteOptionsViewController
        
        toViewController.view.frame.origin = CGPoint(x: toViewController.view.frame.width, y: 0)
        
        transitionContext.containerView()?.addSubview(toViewController.view)
//        
//        let transitioningTextField = fromViewController.searchTextView
//        fromViewController.searchTextView.removeFromSuperview()
//        toViewController.mapTextView = transitioningTextField
//        toViewController.setUpTextView()
//        
//        toViewController.mapView.alpha = 0
        
        UIView.animateWithDuration(transitionDuration(transitionContext), animations: { () -> Void in
            toViewController.view.frame.origin = CGPointZero
            }) { (_) -> Void in
                transitionContext.completeTransition(!transitionContext.transitionWasCancelled())
                toViewController.navigationController?.delegate = toViewController
                toViewController.calculateRoute()
        }
    }
    
}