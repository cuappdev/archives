//
//  RouteOptionsViewController.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import MapKit

class RouteOptionsViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, MKMapViewDelegate, UINavigationControllerDelegate {

    var searchTextView: MapTextField!

    var start: Stop!
    var end: Stop!
    
    var routeOptions: [routeOption]!
    
    var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = UIColor.whiteColor()
        
        print("Found \(routeOptions.count) options")
        
        let backButton = UIButton(frame: CGRect(x: 20, y: kStatusBarHeight, width: 50, height: 44))
        backButton.setTitle("Back", forState: .Normal)
        backButton.setTitleColor(UIColor(red:0.76, green:0.16, blue:0.12, alpha:1), forState: .Normal)
        backButton.addTarget(self, action: "backButtonPressed", forControlEvents: .TouchUpInside)
        view.addSubview(backButton)
        
        let titleLabel = UILabel(frame: CGRect(x: backButton.rightEdge + 20, y: kStatusBarHeight, width: view.frame.width - backButton.rightEdge - 40, height: 44))
        titleLabel.text = "\(start.name) to \(end.name)"
        view.addSubview(titleLabel)
        
        
        let kHeaderHeight: CGFloat = 64
        tableView = UITableView(frame: CGRect(x: 0, y: kHeaderHeight, width: view.frame.width, height: view.frame.height - kHeaderHeight))
        tableView.dataSource = self
        tableView.delegate = self
        
        tableView.registerNib(UINib(nibName: "RouteTableViewCell", bundle: nil), forCellReuseIdentifier: "Cell")
        tableView.rowHeight = 280
        
        view.addSubview(tableView)

    }
    
    func backButtonPressed() {
        navigationController?.popToRootViewControllerAnimated(true)
    }
    
    func calculateRoute() {
        // do shit
        // reloadData()
    }
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return routeOptions.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("Cell", forIndexPath: indexPath) as! RouteTableViewCell
        
        cell.selectionStyle = .None
        
        cell.delegate = self

        let option = routeOptions[indexPath.row]
        cell.setOption(option)
        
        return cell
    }

    // MARK: - MapKitDelegate
    func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
        guard let annotation = annotation as? Stop else { return nil }
        
        let identifier = "pin"
        var view: MKPinAnnotationView
        if let dequeuedView = mapView.dequeueReusableAnnotationViewWithIdentifier(identifier) as? MKPinAnnotationView {
            dequeuedView.annotation = annotation
            view = dequeuedView
        } else {
            view = MKPinAnnotationView(annotation: annotation, reuseIdentifier: identifier)
            view.canShowCallout = true
            view.calloutOffset = CGPoint(x: -5, y: 5)
            //            view.rightCalloutAccessoryView = UIButton(type: .DetailDisclosure)
        }
        
        return view
    }
    
    func mapView(mapView: MKMapView, didSelectAnnotationView view: MKAnnotationView) {
        guard let annotation = view.annotation as? Stop else { return }
        
        print("\(annotation.title) tapped.")
    }

    func navigationController(
        navigationController: UINavigationController,
        animationControllerForOperation
        operation: UINavigationControllerOperation,
        fromViewController
        fromVC: UIViewController,
        toViewController toVC: UIViewController) -> UIViewControllerAnimatedTransitioning? {
            if operation == .Pop {
                return RouteOptionsToMapAnimator.sharedAnimator
            }
            return nil
    }
}
