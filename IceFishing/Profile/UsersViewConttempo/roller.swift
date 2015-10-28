//
//  UsersViewController.swift
//  IceFishing
//
//  Created by Annie Cheng on 4/12/15.
//  Copyright (c) 2015 Lucas Derraugh. All rights reserved.
//

import UIKit

enum DisplayType: String {
	case Followers = "Followers"
	case Following = "Following"
}

class UsersViewController: UITableViewController, UISearchResultsUpdating, UISearchControllerDelegate, UISearchBarDelegate {

	var user: User = User.currentUser
	var displayType: DisplayType = .Followers
	private var users: [User] = []
	private var filteredUsers: [User] = []
	
	private var searchController: UISearchController!

    override func viewDidLoad() {
        super.viewDidLoad()
		
        tableView.registerNib(UINib(nibName: "FollowTableViewCell", bundle: nil), forCellReuseIdentifier: "FollowCell")
		
		searchController = UISearchController(searchResultsController: nil)
		searchController.dimsBackgroundDuringPresentation = false
		searchController.delegate = self
		searchController.searchResultsUpdater = self
		
		//Formating for search Bar
		searchController.searchBar.sizeToFit()
		searchController.searchBar.delegate = self
		searchController.searchBar.searchBarStyle = UISearchBarStyle.Minimal
		searchController.searchBar.tintColor = UIColor.iceDarkRed
		searchController.searchBar.backgroundColor = UIColor.iceDarkRed
		searchController.searchBar.barTintColor = UIColor.iceDarkRed
		
		extendedLayoutIncludesOpaqueBars = true
		definesPresentationContext = true
		
		tableView.tableHeaderView = searchController.searchBar
		tableView.setContentOffset(CGPoint(x: 0, y: searchController.searchBar.frame.size.height), animated: false)

		
		let completion: [User] -> Void = {
			self.users = $0
			self.tableView.reloadData()
		}
		
		if displayType == .Followers {
			API.sharedAPI.fetchFollowers(user.id, completion: completion)
		} else {
			API.sharedAPI.fetchFollowing(user.id, completion: completion)
		}
		
        self.navigationController?.navigationBar.titleTextAttributes = [NSForegroundColorAttributeName: UIColor.whiteColor()]
    }
	
    // Return to previous view
    func popToPrevious() {
        navigationController?.popViewControllerAnimated(true)
    }
    
    // TableView Methods
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
		if searchController.active{
			return self.filteredUsers.count
		} else {
			return self.users.count
		}
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("FollowCell", forIndexPath: indexPath) as! FollowTableViewCell
        
        var user = users[indexPath.row]
		if searchController.active {
			user = filteredUsers[indexPath.row]
		}
        cell.userName.text = user.name
        cell.userHandle.text = "@\(user.username)"
        cell.numFollowLabel.text = "\(user.followersCount) followers"
        user.loadImage {
            cell.userImage.image = $0
        }
        
        return cell
    }
    
    override func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        return 80
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        let selectedCell: UITableViewCell = tableView.cellForRowAtIndexPath(indexPath)!
        selectedCell.contentView.backgroundColor = UIColor.iceLightGray
		let profileVC = ProfileViewController(nibName: "ProfileViewController", bundle: nil)
        profileVC.title = "Profile"
		if searchController.active {
			profileVC.user = filteredUsers[indexPath.row]
		} else {
			profileVC.user = users[indexPath.row]
		}
        self.navigationController?.pushViewController(profileVC, animated: true)
    }
	
	private func filterContentForSearchText(searchText: String, scope: String = "All") {
		if searchText == "" {
			filteredUsers = users
		} else {
			let pred = NSPredicate(format: "name contains[cd] %@", searchText)
			filteredUsers = (users as NSArray).filteredArrayUsingPredicate(pred) as! [User]
		}
		tableView.reloadData()
	}
	
	func updateSearchResultsForSearchController(searchController: UISearchController) {
		filterContentForSearchText(searchController.searchBar.text!)
	}
	
	func searchBarSearchButtonClicked(searchBar: UISearchBar) {
		searchController.searchBar.endEditing(true)
	}
}