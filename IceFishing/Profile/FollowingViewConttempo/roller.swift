//
//  FollowingViewController.swift
//  IceFishing
//
//  Created by Annie Cheng on 4/12/15.
//  Copyright (c) 2015 Lucas Derraugh. All rights reserved.
//

import UIKit

class FollowingViewController: UITableViewController, UIScrollViewDelegate {
    
    // TODO: Uncomment when test user is made
    //var following: [User]! = []
    
    // TODO: For testing purposes (delete when test user is made)
    var following: [String] = ["Derrick", "Eric", "Feifan", "Ilan", "John", "Joe", "Karim", "Lucas", "Manuela", "Mark", "Nicole", "Sam", "Steven", "Tsvi"]
    var followingHandles: [String] = ["derrick", "eric", "feifan", "ilan", "john", "joe", "karim", "lucas", "manuela", "mark", "nicole", "sam", "steven", "tsvi"]
    var numFollowing: [Int] = [10, 229, 38, 40, 100, 374, 2731, 384, 12, 293, 34, 3, 120, 3992]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // TODO: Uncomment when test user is made
        //self.following = User.currentUser.following
        
        tableView.backgroundColor = UIColor.iceDarkGray()
        tableView.registerNib(UINib(nibName: "FollowTableViewCell", bundle: nil), forCellReuseIdentifier: "FollowCell")
        
        tableView.separatorStyle = .None
        
        self.navigationController?.navigationBar.barTintColor = UIColor.iceDarkRed()
        self.navigationController?.navigationBar.titleTextAttributes = [NSForegroundColorAttributeName: UIColor.whiteColor()]
        
        // Add back button to profile
        var backButton = UIButton(frame: CGRect(x: 0, y: 0, width: 25, height: navigationController!.navigationBar.frame.height))
        backButton.setImage(UIImage(named: "Close-Icon"), forState: .Normal)
        backButton.addTarget(self, action: "popToRoot", forControlEvents: .TouchUpInside)
        navigationItem.leftBarButtonItem = UIBarButtonItem(customView: backButton)
    }
    
    // Return to profile view
    func popToRoot() {
        navigationController?.popToRootViewControllerAnimated(true)
    }
    
    // TableView Methods
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.following.count
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("FollowCell", forIndexPath: indexPath) as! FollowTableViewCell
        
        // TODO: For testing purposes (delete when test user is made)
        cell.userImage.image = UIImage(named: "Steven")
        cell.userName.text = self.following[indexPath.row]
        cell.userHandle.text = "@\(self.followingHandles[indexPath.row])"
        cell.numFollowLabel.text = "\(self.numFollowing[indexPath.row]) followers"
        
        // TODO: Uncomment when test user is made
        //        cell.userImage.image = self.following[indexPath.row].profileImage
        //        cell.userName.text = self.following[indexPath.row].name
        //        cell.userHandle.text = "@\(self.following[indexPath.row].username)"
        //        cell.numFollowLabel.text = "\(self.following[indexPath.row].followersCount) followers"
        
        
        return cell
    }
    
    override func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        return CGFloat(80)
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        var selectedCell:UITableViewCell = tableView.cellForRowAtIndexPath(indexPath)!
        selectedCell.contentView.backgroundColor = UIColor.iceLightGray()
        
        // TODO: Push to user's profile view
    }    
}
