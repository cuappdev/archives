//
//  RouteOptionsViewController.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class RouteOptionsViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {

    var searchTextView: MapTextField!

    var start: Stop!
    var end: Stop!
    
    var routeOptions: [routeOption]!
    
    var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = UIColor.whiteColor()
        
        print("Found \(routeOptions.count) options")
        
        let kHeaderHeight: CGFloat = 20
        tableView = UITableView(frame: CGRect(x: 0, y: kHeaderHeight, width: view.frame.width, height: view.frame.height - kHeaderHeight))
        tableView.dataSource = self
        tableView.delegate = self
        
        tableView.registerClass(UITableViewCell.self, forCellReuseIdentifier: "Cell")
        
        view.addSubview(tableView)

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
        let cell = tableView.dequeueReusableCellWithIdentifier("Cell", forIndexPath: indexPath)
        
        let option = routeOptions[indexPath.row]
        
        cell.textLabel?.text = "[\(option.route.id)] \(option.stops.first!.time)-\(option.stops.last!.time) (\(option.stops.count-1) stops)"
        
        return cell
    }

    
}
