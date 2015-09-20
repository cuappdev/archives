//
//  MainViewController-UIGestureRecognizerDelegate.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import MapKit

extension MainViewController: UIGestureRecognizerDelegate {
    func gestureRecognizer(gestureRecognizer: UIGestureRecognizer, shouldRecognizeSimultaneouslyWithGestureRecognizer otherGestureRecognizer: UIGestureRecognizer) -> Bool {
        return true
    }
    
    func didPanMap(sender: UIPanGestureRecognizer) {
        updateMapFocus()

//        switch sender.state {
//        case .Changed:
//            updateMapFocus()
//        default:
//            print("default")
//        }
    }
    
    func updateMapFocus() {
        func checkAnnotationsEqual(a: MKAnnotation?, b: MKAnnotation) -> Bool {
            guard a != nil else { return false }
            
            return a!.title! == b.title!
        }
        
        func resetAnnotationToIdentity(annotation: MKAnnotation?) {
            if let a = annotation {
                if let prevView = mapView.viewForAnnotation(a) {
                    prevView.transform = CGAffineTransformIdentity
                    prevView.image = UIImage(named: "redPin")
                }
            }
        }
        
        let prevFocusedAnnotation = focusedAnnotation
        let newFocusedAnnotation = findClosestAnnotation()
        
        let annotationsEqual = checkAnnotationsEqual(prevFocusedAnnotation, b: newFocusedAnnotation)
        if !annotationsEqual {
            resetAnnotationToIdentity(prevFocusedAnnotation)
            
            if let newFocusView = mapView.viewForAnnotation(newFocusedAnnotation) {
                focusedAnnotation = newFocusedAnnotation // do this in completion block?
                UIView.animateWithDuration(0.3, delay: 0, usingSpringWithDamping: 0.3, initialSpringVelocity: 0, options: [], animations: { () -> Void in
                    newFocusView.transform = CGAffineTransformMakeScale(1.5, 1.5)
                    newFocusView.image = UIImage(named: "bluePin")
                    }, completion: nil)
            }
        }
        
        if activeSearchField == .Start {
            mapTextView.startTextField.text = focusedAnnotation!.title!!
        } else {
            mapTextView.endTextField.text = focusedAnnotation!.title!!
        }
        
        showBussesView()
    }
    
    private func findClosestAnnotation() -> MKAnnotation {
        let centerLocation = CLLocation(latitude: mapView.centerCoordinate.latitude, longitude: mapView.centerCoordinate.longitude)
        var closestAnnotation = mapView.annotations[0]
        let closestAnnotationLocation = CLLocation(latitude: closestAnnotation.coordinate.latitude, longitude: closestAnnotation.coordinate.longitude)
        var closestDistance = closestAnnotationLocation.distanceFromLocation(centerLocation)
        for annotation in mapView.annotations {
            if !annotation.isMemberOfClass(MKUserLocation) {
                let annotationLocation = CLLocation(latitude: annotation.coordinate.latitude, longitude: annotation.coordinate.longitude)
                let distance = annotationLocation.distanceFromLocation(centerLocation)
                if distance < closestDistance {
                    closestAnnotation = annotation
                    closestDistance = distance
                }
            }
        }
        
        return closestAnnotation
    }
}