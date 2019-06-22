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
        transitioningTextField.startTextField.delegate = toViewController
        transitioningTextField.endTextField.delegate = toViewController
        transitioningTextField.delegate = nil

//        transitioningTextField.endEditing(true)
        fromViewController.mapTextView.removeFromSuperview()
        toViewController.searchTextView = transitioningTextField
        toViewController.view.addSubview(transitioningTextField)
        toViewController.stops = fromViewController.stops
        transitioningTextField.startTextField.addTarget(toViewController, action: "updateSearchResultsForTextField:", forControlEvents: .EditingChanged)
        transitioningTextField.endTextField.addTarget(toViewController, action: "updateSearchResultsForTextField:", forControlEvents: .EditingChanged)

        toViewController.tableView.alpha = 0
        
        let kTextFieldYOffset: CGFloat = 10
        let newTextFieldFrame = CGRect(x: 0, y: transitioningTextField.frame.origin.y, width: toViewController.view.frame.width, height: transitioningTextField.frame.height + kTextFieldYOffset)
        toViewController.tableView.frame = CGRect(x: 0, y: newTextFieldFrame.origin.y + newTextFieldFrame.height, width: toViewController.view.frame.width, height: toViewController.view.frame.height - newTextFieldFrame.origin.y - newTextFieldFrame.height)
        UIView.animateWithDuration(transitionDuration(transitionContext), animations: { () -> Void in
            transitioningTextField.frame = newTextFieldFrame
            toViewController.tableView.alpha = 1
            }) { (_) -> Void in
                transitionContext.completeTransition(!transitionContext.transitionWasCancelled())
                toViewController.navigationController?.delegate = toViewController
                if activeSearchField == .Start {
                    transitioningTextField.startTextField.becomeFirstResponder()
                    toViewController.updateSearchResultsForTextField(transitioningTextField.startTextField)
                } else {
                    transitioningTextField.endTextField.becomeFirstResponder()
                    toViewController.updateSearchResultsForTextField(transitioningTextField.endTextField)
                }
        }
    }
}
