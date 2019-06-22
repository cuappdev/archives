//
//  SearchToMapAnimator.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class SearchToMapAnimator: NSObject, UIViewControllerAnimatedTransitioning {
    static let sharedAnimator = SearchToMapAnimator()
    
    func transitionDuration(transitionContext: UIViewControllerContextTransitioning?) -> NSTimeInterval {
        return 0.2
    }
    
    func animateTransition(transitionContext: UIViewControllerContextTransitioning) {
        let toViewController = transitionContext.viewControllerForKey(UITransitionContextToViewControllerKey) as! MainViewController
        let fromViewController = transitionContext.viewControllerForKey(UITransitionContextFromViewControllerKey) as! SearchViewController
        
        transitionContext.containerView()?.addSubview(toViewController.view)
        
        let transitioningTextField = fromViewController.searchTextView
        fromViewController.searchTextView.removeFromSuperview()
        toViewController.mapTextView = transitioningTextField
        toViewController.setUpTextView()
        
        toViewController.mapView.alpha = 0

        UIView.animateWithDuration(transitionDuration(transitionContext), animations: { () -> Void in
            transitioningTextField.frame = toViewController.textViewFrame
            toViewController.mapView.alpha = 1
            }) { (_) -> Void in
                transitionContext.completeTransition(!transitionContext.transitionWasCancelled())
                toViewController.navigationController?.delegate = toViewController
        }
    }

}
