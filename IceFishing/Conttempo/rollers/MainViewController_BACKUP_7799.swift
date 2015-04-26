//
//  ViewController.swift
//  IceFishingTrending
//
//  Created by Joseph Antonakakis on 3/8/15.
//  Copyright (c) 2015 Joseph Antonakakis. All rights reserved.
//

import UIKit

class MainViewController: UIViewController, SearchTrackResultsViewControllerDelegate, UISearchControllerDelegate {

    let options: UISegmentedControl = UISegmentedControl(items: ["Songs", "Users"])
    
    var childVC1 = FeedViewController(nibName: "FeedViewController", bundle: nil)
<<<<<<< HEAD

    var searchController: TrackSearchController!
    var searchResultsController: SearchTrackResultsViewController!
    var preserveTitleView: UIView!
=======
    //var childVC2 = TrendingViewController()
    var searchController: UISearchController!
    var searchNavigationController: UINavigationController!
>>>>>>> 97f6f4809270e30817b1959e5b108f4dcaf487b7
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Add Songs/Users option element to the navbar
        options.selectedSegmentIndex = 0
        options.tintColor = UIColor.grayColor()
        options.addTarget(self, action: "switchTable", forControlEvents: .ValueChanged)
//        navigationItem.titleView = options
        
        navigationItem.title = "Songs"
        addPlusButton()
        
        addChildViewController(childVC1)
        childVC1.view.frame = view.bounds
        view.addSubview(childVC1.view)
        
        navigationController?.navigationBar.barTintColor = UIColor(red: 181.0 / 255.0, green: 87.0 / 255.0, blue: 78.0 / 255.0, alpha: 1.0)
        navigationController?.navigationBar.tintColor = UIColor.whiteColor()
        navigationController?.navigationBar.barStyle = .Black
//        navigationController?.navigationBar.translucent = true
        
        // Add profile button to the left side of the navbar
        var profileButton = UIButton(frame: CGRect(x: 0, y: 0, width: 25, height: navigationController!.navigationBar.frame.height * 0.65))
        profileButton.setImage(UIImage(named: "white-hamburger-menu-Icon"), forState: .Normal)
//        profileButton.addTarget(self, action: "pushToProfile", forControlEvents: .TouchUpInside)
        profileButton.addTarget(self.revealViewController(), action: "revealToggle:", forControlEvents: .TouchUpInside)
        
        if self.revealViewController() != nil {
            self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
        }

        navigationItem.leftBarButtonItem = UIBarButtonItem(customView: profileButton)
        
        // Arbitrary additions for SWRevealVC
        revealViewController().panGestureRecognizer()
        revealViewController().tapGestureRecognizer()
        
    }
    
<<<<<<< HEAD
    func switchTable() {
        if (options.selectedSegmentIndex == 1 && childViewControllers[0] as! NSObject == childVC1) {
            childVC1.view.removeFromSuperview() //Removes it from view
            childVC1.removeFromParentViewController() //Removes it as child
            childVC2.view.frame = view.bounds
            addChildViewController(childVC2) //Adds as child
            view.addSubview(childVC2.view) //Adds to view
        } else if (options.selectedSegmentIndex == 0 && childViewControllers[0] as! NSObject == childVC2) {
            childVC2.view.removeFromSuperview()
            childVC2.removeFromParentViewController()
            addChildViewController(childVC1)
            childVC1.view.frame = view.bounds
            view.addSubview(childVC1.view)
        }
    }
=======
    // Add profile button
//    func pushToProfile() {
//        let loginViewController = LoginViewController(nibName: "LoginViewController", bundle: nil)
//        var feedButton = UIButton(frame: CGRect(x: 0, y: 0, width: 25, height: navigationController!.navigationBar.frame.height * 0.65))
//        feedButton.setImage(UIImage(named: "white-hamburger-menu-Icon"), forState: .Normal)
//        feedButton.addTarget(self, action: "closeProfileView", forControlEvents: .TouchUpInside)
//        loginViewController.navigationItem.leftBarButtonItem = UIBarButtonItem(customView: feedButton)
//
//        searchNavigationController = UINavigationController(rootViewController: loginViewController)
//        presentViewController(searchNavigationController, animated: false, completion: nil)
//    }
    
    func initializePostCreation() {
        var searchResultsViewController = SearchTrackResultsViewController() as SearchTrackResultsViewController
        
        let searchViewController = SearchTrackViewController()
        searchNavigationController = UINavigationController(rootViewController: searchViewController)
>>>>>>> 97f6f4809270e30817b1959e5b108f4dcaf487b7

    func addPlusButton() {
        // Add plus sign to the right side of the navbar
        let button = UIBarButtonItem(barButtonSystemItem: UIBarButtonSystemItem.Add, target: self, action: "initializePostCreation")
        navigationItem.rightBarButtonItem = button
    }

    func initializePostCreation() {
        searchResultsController = SearchTrackResultsViewController() as SearchTrackResultsViewController
        
        searchController = TrackSearchController(searchResultsController: searchResultsController)
        searchController.searchResultsUpdater = searchResultsController
        searchController.delegate = self
        searchController.parent = self
        searchResultsController.delegate = self
        definesPresentationContext = true
        
        preserveTitleView = navigationItem.titleView
        navigationItem.titleView = searchController.searchBar
        navigationItem.rightBarButtonItem = nil
        
        delay(0.05) {
            self.searchController.searchBar.becomeFirstResponder()
            return
        }
    }
    
    func willDismissSearchController(searchController: UISearchController) {
        navigationItem.titleView = preserveTitleView
        addPlusButton()
    }
    
    func selectSong(track: TrackResult) {
        searchController?.showResultSelection(track)
    }
    
    func postSong(track: TrackResult) {
        closeSearchView()
        childVC1.addSong(track)
        searchController.active = false
        
        searchResultsController.finishSearching()
        
        println("TODO: add this track")
        println(track)
    }
    
    func closeProfileView() {
        searchNavigationController?.dismissViewControllerAnimated(true, completion: nil)
    }
    
    func closeSearchView() {
        searchController?.searchBar.text = ""
        searchController?.searchBar.resignFirstResponder()
        searchResultsController.finishSearching()
    }
}
