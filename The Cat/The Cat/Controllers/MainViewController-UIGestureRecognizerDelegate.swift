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
    
    @available(iOS 9.0, *)
    func didPanMap(sender: UIPanGestureRecognizer) {
        switch sender.state {
        case .Changed:
            
            if let prevFocused = focusedAnnotation {
                focusedAnnotation = findClosestAnnotation()
                guard !focusedAnnotation!.isEqual(prevFocused) else { return }
                
                if let prevFocusedAnnotationView = mapView.viewForAnnotation(prevFocused) {
                    prevFocusedAnnotationView.transform = CGAffineTransformIdentity
                    if let v = prevFocusedAnnotationView as? MKPinAnnotationView {
                        v.pinTintColor = MKPinAnnotationView.redPinColor()
                    }
                }
                
                if let focusedAnnotationView = mapView.viewForAnnotation(focusedAnnotation!) {
                    UIView.animateWithDuration(0.1, animations: { () -> Void in
                        focusedAnnotationView.transform = CGAffineTransformMakeScale(1, 1.5)
                        if let v = focusedAnnotationView as? MKPinAnnotationView {
                            v.pinTintColor = MKPinAnnotationView.greenPinColor()
                        }
                        }, completion: { (finished) -> Void in
                            UIView.animateWithDuration(0.15, animations: { () -> Void in
                                focusedAnnotationView.transform = CGAffineTransformMakeScale(1, 1.25)
                            })
                    })
                }
            }
            
            focusedAnnotation = findClosestAnnotation()
            let focusedAnnotationView = mapView.viewForAnnotation(focusedAnnotation!)!
            
            UIView.animateWithDuration(0.1, animations: { () -> Void in
                focusedAnnotationView.transform = CGAffineTransformMakeScale(1, 1.5)
                if let v = focusedAnnotationView as? MKPinAnnotationView {
                    v.pinTintColor = MKPinAnnotationView.greenPinColor()
                }
                }, completion: { (finished) -> Void in
                    UIView.animateWithDuration(0.15, animations: { () -> Void in
                        focusedAnnotationView.transform = CGAffineTransformMakeScale(1, 1.25)
                    })
            })
            
//            focusedAnnotation!.
            
        default:
            print("default")
        }
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