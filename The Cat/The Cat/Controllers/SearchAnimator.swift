//
//  SearchAnimator.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class SearchAnimator: NSObject, UIViewControllerAnimatedTransitioning {
    static let sharedAnimator = SearchAnimator()

    func transitionDuration(transitionContext: UIViewControllerContextTransitioning?) -> NSTimeInterval {
        return 0.2
    }
    
    func animateTransition(transitionContext: UIViewControllerContextTransitioning) {
        let toViewController = transitionContext.viewControllerForKey(UITransitionContextToViewControllerKey) as! SearchViewController
        let fromViewController = transitionContext.viewControllerForKey(UITransitionContextFromViewControllerKey) as! MainViewController
        
        transitionContext.containerView()?.addSubview(toViewController.view)
        let transitioningTextField = fromViewController.mapTextView
        transitioningTextField.startTextField.delegate = nil
        transitioningTextField.endTextField.delegate = nil

//        transitioningTextField.endEditing(true)
        fromViewController.mapTextView.removeFromSuperview()
        toViewController.searchTextView = transitioningTextField
        toViewController.view.addSubview(transitioningTextField)
        toViewController.stops = fromViewController.stops
        toViewController.filteredStops = fromViewController.stops
        transitioningTextField.startTextField.addTarget(toViewController, action: "updateSearchResultsForTextField:", forControlEvents: .EditingChanged)
        transitioningTextField.endTextField.addTarget(toViewController, action: "updateSearchResultsForTextField:", forControlEvents: .EditingChanged)

        toViewController.tableView.alpha = 0
        
        let kTextFieldYOffset: CGFloat = 10
        let newTextFieldFrame = CGRect(x: 0, y: transitioningTextField.frame.origin.y, width: toViewController.view.frame.width, height: transitioningTextField.frame.height + kTextFieldYOffset)
        UIView.animateWithDuration(transitionDuration(transitionContext), animations: { () -> Void in
            transitioningTextField.frame = newTextFieldFrame
            toViewController.tableView.alpha = 1
            }) { (_) -> Void in
                transitionContext.completeTransition(!transitionContext.transitionWasCancelled())
                if activeSearchField == .Start {
                    transitioningTextField.startTextField.becomeFirstResponder()
                } else {
                    transitioningTextField.endTextField.becomeFirstResponder()
                }
        }
    }
}
