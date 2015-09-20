//
//  MainViewController-UINavigationControllerDelegate.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

extension MainViewController: UINavigationControllerDelegate {
    func navigationController(
        navigationController: UINavigationController,
        animationControllerForOperation
        operation: UINavigationControllerOperation,
        fromViewController
        fromVC: UIViewController,
        toViewController toVC: UIViewController) -> UIViewControllerAnimatedTransitioning? {
            if toVC.isKindOfClass(SearchViewController.self) {
                return SearchAnimator.sharedAnimator
            } else if toVC.isKindOfClass(RouteOptionsViewController.self) {
             return RouteOptionsAnimator.sharedAnimator
            }
            
            return nil
    }
}