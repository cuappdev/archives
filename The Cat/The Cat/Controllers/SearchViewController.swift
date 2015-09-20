//
//  SearchViewController.swift
//  The Cat
//
//  Created by Eric Appel on 9/18/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import CoreLocation

class SearchViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UITextFieldDelegate {
    
    var searchTextView: MapTextField!
    
    var stops: [Stop] = []
    var filteredStops: [Stop] = []
    
    var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
                
        let statusBarView = UIView(frame: CGRect(x: 0, y: 0, width: view.frame.width, height: 20))
        statusBarView.backgroundColor = UIColor.whiteColor()
        view.addSubview(statusBarView)
        
//        view.backgroundColor = UIColor.redColor()
        
        tableView = UITableView(frame: CGRectZero)
        tableView.dataSource = self
        tableView.delegate = self

        tableView.registerNib(UINib(nibName: "StopTableViewCell", bundle: nil), forCellReuseIdentifier: "Cell")
        tableView.rowHeight = 54
        
        view.addSubview(tableView)
        
        filteredStops = stops
    }
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return filteredStops.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("Cell", forIndexPath: indexPath) as! StopTableViewCell
        
        let stop = filteredStops[indexPath.row]
        var distance = ""
        if let userLocation = locationManager.location {
            var miles = CLLocation(latitude: stop.coordinate.latitude, longitude: stop.coordinate.longitude).distanceFromLocation(userLocation) / 1609.34
            miles = round(10.0 * miles) / 10
            distance = "\(miles) mi"
        }
        
        cell.setStop(stop, distanceString: "\(distance)")
        
        return cell
    }
    
    // MARK: -
    // MARK: TableView delegate
    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        tableView.deselectRowAtIndexPath(indexPath, animated: true)
        
        let stop = filteredStops[indexPath.row]
        
        
        
        if activeSearchField == .Start {
            searchTextView.startTextField.text = stop.name
        } else {
            searchTextView.endTextField.text = stop.name
            dispatchAfter(0.5, block: { () -> Void in
                self.navigationController?.popToRootViewControllerAnimated(true)
            })
        }
    }
    
    // MARK: -
    // MARK: UISearchResultsUpdating
    
    func filterContentForSearchText(searchText: String, scope: String = "All") {
        if searchText == "" {
            filteredStops = stops
        } else {
            filteredStops = stops.filter({ (stop: Stop) -> Bool in
                return stopsEquiv(searchText, b: stop.name)
            })
            print(filteredStops)
        }
        tableView.reloadData()
    }
    
    func updateSearchResultsForTextField(sender: UITextField) {
        if sender == searchTextView.startTextField {
            activeSearchField = .Start
        } else {
            activeSearchField = .End
        }
        print(sender.text ?? "")
        filterContentForSearchText(sender.text ?? "")
    }
    
    // MARK: -
    // MARK: Text Field Delegate
    
    func textFieldDidBeginEditing(textField: UITextField) {
        if textField == searchTextView.startTextField {
            activeSearchField = .Start
        } else {
            activeSearchField = .End
        }
        updateSearchResultsForTextField(textField)
    }
    
    func scrollViewDidScroll(scrollView: UIScrollView) {
        view.endEditing(true)
    }
    
//    // MARK: -
//    // MARK: UISearchControllerDelegate
//    
//    /// Search content will scroll behind status bar so add a cover-up view to mask it
//    private let statusBarView: UIView = {
//        let view = UIView(frame: CGRect(x: 0, y: 0, width: UIScreen.mainScreen().bounds.width, height: 20))
//        view.backgroundColor = UIColor.whiteColor()
//        return view
//        }()
//    
//    func willPresentSearchController(searchController: UISearchController) {
//        dispatchAfter(0.4, block: { () -> Void in
//            navigationController?.view.addSubview(statusBarView)
//        })
//    }
//    
//    func didDismissSearchController(searchController: UISearchController) {
//        statusBarView.removeFromSuperview()
//    }
//    
//    func searchBarSearchButtonClicked(searchBar: UISearchBar) {
//        searchController.searchBar.endEditing(true)
//    }


}
