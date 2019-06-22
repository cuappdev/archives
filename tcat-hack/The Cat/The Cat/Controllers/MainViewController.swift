//
//  MainViewController.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import MapKit

class MainViewController: UIViewController, UITextFieldDelegate, TextSearchDelegate {

    var mapTextView: MapTextField!
//    let endTextField = UITextField()
    
    var focusedAnnotation: MKAnnotation?
    
    var mapView: MKMapView!
    var findBussesView: FindBussesView!
    
    var routeDict: [Int:Route]!
    
    var stops: [Stop] = []
    
    var centerLocationButton: UIButton!
    var centerLocationButtonOffset = false
    
    var textViewFrame: CGRect {
        let kTextFieldHeight: CGFloat = 115
        let kTextFieldEdgeInsets = UIEdgeInsets(top: 0, left: 10, bottom: 10, right: 10)
        let textViewFrame = CGRect(
            x: kTextFieldEdgeInsets.left,
            y: kStatusBarHeight + kTextFieldEdgeInsets.top,
            width: view.frame.width - kTextFieldEdgeInsets.left - kTextFieldEdgeInsets.right,
            height: kTextFieldHeight)
        
        return textViewFrame
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Navigation
        navigationController?.delegate = self
        
        // MapView
        mapView = MKMapView(frame: view.frame)
        mapView.delegate = self
        mapView.showsUserLocation = true
        
        let panGesture = UIPanGestureRecognizer(target: self, action: "didPanMap:")
        panGesture.delegate = self
        mapView.addGestureRecognizer(panGesture)
        
        view.addSubview(mapView)
        
        checkLocationAuthorizationStatus()
        
        centerOnCurrentLocation()
        
        do {
            let stopsArray = try initializeStops()
            stops = stopsArray
            for stop in stopsArray {
                mapView.addAnnotation(stop)
                stopsDict[stop.name] = stop
            }
        } catch {
            print("Error parsing stops-locations json file")
        }
        
        routeDict = try! initializeRoutes()
//        do {
//            routeDict = try! initializeRoutes()
//            print("break")
//            getThreeOptions(nil, end: nil, routeDict: routeDict)
//            
//        } catch {
//            print("Error parsing route-schedules json file")
//        }
        
        // Status Bar
//        let statusBarBackgroundView = UIView(frame: CGRect(x: 0, y: 0, width: view.frame.width, height: 20))
//        statusBarBackgroundView.backgroundColor = UIColor.whiteColor()
//        view.addSubview(statusBarBackgroundView)
        
        // Text Fields
        mapTextView = NSBundle.mainBundle().loadNibNamed("MapTextField", owner: self, options: nil).first as! MapTextField
        setUpTextView()
        setUpLocationButton()
        mapTextView.frame = textViewFrame
//        mapTextView.startTextField.text = "Baker Flagpole"
//        mapTextView.endTextField.text = "East Hill Plaza"
        
        mapTextView.layer.shadowColor = UIColor.blackColor().CGColor
        mapTextView.layer.shadowOffset = CGSizeZero
        mapTextView.layer.shadowOpacity = 0.5
        mapTextView.layer.shadowRadius = 1
        
        // Find busses
        let kFindBussesHeight: CGFloat = 75
        let findBussesFrame = CGRect(x: 0, y: view.frame.height, width: view.frame.width, height: kFindBussesHeight)
        findBussesView = NSBundle.mainBundle().loadNibNamed("FindBussesView", owner: self, options: nil).first as! FindBussesView
        findBussesView.frame = findBussesFrame
        findBussesView.actionButton.addTarget(self, action: "findBussesPressed", forControlEvents: .TouchUpInside)
        view.addSubview(findBussesView)
    }
    
    func setUpTextView() {
        mapTextView.startTextField.delegate = self
        mapTextView.endTextField.delegate = self
        mapTextView.delegate = self
        view.addSubview(mapTextView)
    }
    
    func setUpLocationButton() {
        let xOffset = 80
        let yOffset = 80
        centerLocationButton = UIButton(type: .Custom)
        centerLocationButton.frame = CGRectMake(UIScreen.mainScreen().bounds.width - CGFloat(xOffset), UIScreen.mainScreen().bounds.height - CGFloat(yOffset), 50, 50)
        centerLocationButton.setImage(UIImage(named: "locationicon"), forState: .Normal)
        centerLocationButton.addTarget(self, action: "centerLocationButtonPressed:", forControlEvents: UIControlEvents.TouchUpInside)
        view.addSubview(centerLocationButton)
    }
    
    func centerLocationButtonPressed(sender: UIButton) {
        centerOnCurrentLocation()
    }
    
    func centerOnCurrentLocation() {
        let initialLocation = mapView.userLocation.location ?? CLLocation(latitude: 42.4433, longitude: -76.5000)
        let regionRadius: CLLocationDistance = 750
        centerMapOnLocation(initialLocation, regionRadius: regionRadius)
    }
    
    func getThreeOptions(start: String, end: String, routeDict: [Int:Route]) -> [routeOption] {
//        let start = "Airport"
//        let end = "East Hill Plaza" //"East Hill Plaza"
        var options: [routeOption] = []
        var now = NSDate()
        let nowString = dateToTime(now)
//        let nowString = "12:35PM"
        now = timeToDate(nowString)!
        
        func findDestination(instance: [RouteStop]) -> [RouteStop]? {
            for (index, element) in instance.enumerate() {
                // Need to check here for slight equivalence
                // i.e. (Baker Flagpole) == (Baker Flagpole/Slopeside) = true
                if stopsEquiv(element.stopName, b: start) { break }
                
                if element.stopName == end {
                    return Array(instance.prefixUpTo(index+1))
                }
            }
            return nil
        }
        
        for r in Array(routeDict.values) {
            if r.stops.contains(start) && r.stops.contains(end) {
                for (instanceIndex, instance) in r.schedule.enumerate() {
                    for (stopIndex, instanceStop) in instance.enumerate() {
                        if stopsEquiv(instanceStop.stopName, b: start) {
                            if instanceStop != instance.last! {
                                let nextStopsInInstance = Array(instance.suffixFrom(stopIndex+1))
                                if let option = findDestination(nextStopsInInstance) {
                                    let tuple = (r, [instanceStop] + option)
                                    options.append(tuple)
                                } else {
                                    // If we cant find the destination in the rest of the route instance,
                                    // check the next instance since the route must be a loop becasue we
                                    // already checked that the route services both stops
                                    guard instance != r.schedule.last! else { continue }
                                    let nextInstance = r.schedule[instanceIndex+1]
                                    if let option = findDestination(nextInstance) {
                                        let tuple = (r, [instanceStop] + nextStopsInInstance + option)
                                        options.append(tuple)
                                    }
                                }
                            } else {
                                // If stop is the last in the instance, we dont need to look for the destination in nextStopsInInstance
                                guard instance != r.schedule.last! else { continue }
                                let nextInstance = r.schedule[instanceIndex+1]
                                if let option = findDestination(nextInstance) {
                                    let tuple = (r, [instanceStop] + option)
                                    options.append(tuple)
                                }
                            }
                            
                        }
                    }
                }
            }
        }
        
        // Filter out stops with invalid times
        options = options.filter({ (option: routeOption) -> Bool in
            if now.compare(option.stops.first!.date) == .OrderedAscending {
                if now.compare(option.stops.last!.date) == .OrderedAscending {
                    return true
                }
            }
            return false
        })
        
        // Sort options by arrival time
        options = options.sort { (first: routeOption, second: routeOption) -> Bool in
            let firstTime = first.stops.last!.date
            let secondTime = second.stops.last!.date
            
            if firstTime.compare(secondTime) == .OrderedDescending {
                return false
            }
            
            return true
        }
        
//        let printableOptions = options.map { (option: routeOption) -> [RouteStop] in
//            return option.stops
//        }
//        print(printableOptions[0])
        
        return options
    }
    
    private func initializeStops() throws -> [Stop] {
        let filePath = NSBundle.mainBundle().pathForResource("stop-locations", ofType: "json")!
        let stopData = NSData(contentsOfFile: filePath)!
        
        do {
            let jsonData = try NSJSONSerialization.JSONObjectWithData(stopData, options: [])
            let jsonStops = JSON(rawValue: jsonData)!
            
            let stopsJSONArray = jsonStops.arrayValue
            var stopsArray: [Stop] = []
            for stopJSON in stopsJSONArray {
                if let stop = Stop(json: stopJSON) {
                    stopsArray.append(stop)
                }
            }
            return stopsArray
        } catch {
            throw NSError(domain: "tcat", code: 400, userInfo: nil)
        }
    }
    
    private func initializeRoutes() throws -> [Int:Route] {
        let routeNumbers = [11,13,14,15,17,20,21,30,31,32,36,37,40,41,43,51,52,53,65,67,70,72,74,75,77,81,82,83,92]

        var routesDict: [Int:Route] = [:]
        for id in routeNumbers {
            routesDict[id] = Route(id: id)
        }
        
        let filePath = NSBundle.mainBundle().pathForResource("route-schedules", ofType: "json")!
        let stopData = NSData(contentsOfFile: filePath)!
        
        do {
            let jsonData = try NSJSONSerialization.JSONObjectWithData(stopData, options: [])
            let jsonStops = JSON(rawValue: jsonData)!
            
            let stopsJSONArray = jsonStops.arrayValue
            for stopJSON in stopsJSONArray {
                if let stop = RouteStop(json: stopJSON) {
                    guard stop.day == "Sunday" || stop.day == "Weekends" else { continue }
                    if let route = routesDict[stop.route] {
                        if route.schedule.count == 0 {
                            route.schedule.append([stop])
                        } else {
                            if route.schedule.last!.last!.instance == stop.instance {
                                route.schedule[route.schedule.count-1].append(stop)
                            } else {
                                route.schedule.append([stop])
                            }
                        }
                        route.stops.insert(stop.stopName)
                    }
                }
            }
            return routesDict
        } catch {
            throw NSError(domain: "tcat", code: 400, userInfo: nil)
        }
    }
    
    private func centerMapOnLocation(location: CLLocation, regionRadius: CLLocationDistance) {
        let coordinateRegion = MKCoordinateRegionMakeWithDistance(location.coordinate,
            regionRadius * 2.0, regionRadius * 2.0)
        mapView.setRegion(coordinateRegion, animated: true)
    }

    private func checkLocationAuthorizationStatus() {
        if CLLocationManager.authorizationStatus() != .AuthorizedWhenInUse {
            locationManager.requestWhenInUseAuthorization()
        }
        locationManager.distanceFilter = kCLDistanceFilterNone // whenever we move
        locationManager.desiredAccuracy = kCLLocationAccuracyBest 
        locationManager.startUpdatingLocation()
    }
    
    // MARK: - Text Field Stuff
    func textFieldShouldBeginEditing(textField: UITextField) -> Bool {
        if textField == mapTextView.startTextField {
            activeSearchField = .Start
        } else {
            activeSearchField = .End
        }
        
        return false
    }
    
    func startFieldSearch() {
        activeSearchField = .Start

        let searchVC = SearchViewController()
        searchVC.searchTextView = mapTextView
        navigationController?.pushViewController(searchVC, animated: true)
    }
    
    func endFieldSearch() {
        activeSearchField = .End
        
        let searchVC = SearchViewController()
        searchVC.searchTextView = mapTextView
        navigationController?.pushViewController(searchVC, animated: true)
    }
    
    override func viewDidAppear(animated: Bool) {
        guard !mapTextView.startTextField.text!.isEmpty else { return }
        guard !mapTextView.endTextField.text!.isEmpty else { return }
        
        showBussesView()
    }
    
    func showBussesView() {
        guard !mapTextView.startTextField.text!.isEmpty else { return }
        guard !mapTextView.endTextField.text!.isEmpty else { return }
        if findBussesView.frame.origin.y >= view.frame.height {
            UIView.animateWithDuration(0.2) { () -> Void in
                self.findBussesView.frame.origin = CGPoint(x: 0, y: self.view.frame.height - self.findBussesView.frame.height)
            }
        }
        if (!centerLocationButtonOffset) {
            centerLocationButton!.center.y -= findBussesView.frame.height
            centerLocationButtonOffset = true
        }
    }
    
    func findBussesPressed() {
        let start = mapTextView.startTextField.text!
        let end = mapTextView.endTextField.text!
        print("find route for \(start) -> \(end)")
        // Start loading indicator
        let routeOptionsVC = RouteOptionsViewController()
        routeOptionsVC.routeOptions = getThreeOptions(mapTextView.startTextField.text!, end: mapTextView.endTextField.text!, routeDict: routeDict)
        if routeOptionsVC.routeOptions.count == 0 {
            let alert = UIAlertView(title: "No route found", message: "There are no direct routes from \(start) tp \(end)", delegate: nil, cancelButtonTitle: "OK")
            alert.show()
        } else {
            routeOptionsVC.start = stopsDict[start]
            routeOptionsVC.end = stopsDict[end]
            navigationController?.pushViewController(routeOptionsVC, animated: true)
        }
    }
}



