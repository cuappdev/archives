//
//  SearchViewController-UINavigationControllerDelegate.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

extension SearchViewController: UINavigationControllerDelegate {
    func navigationController(
        navigationController: UINavigationController,
        animationControllerForOperation
        operation: UINavigationControllerOperation,
        fromViewController
        fromVC: UIViewController,
        toViewController toVC: UIViewController) -> UIViewControllerAnimatedTransitioning? {
            if operation == .Pop {
                return SearchToMapAnimator.sharedAnimator
            }
            return nil
    }
}