//
//  UsernameViewController.swift
//  IceFishing
//
//  Created by Manuela Rios on 4/8/15.
//  Copyright (c) 2015 Lucas Derraugh. All rights reserved.
//

import UIKit

class UsernameViewController: UIViewController {
 
    var searchNavigationController: UINavigationController!
    let api = API.sharedAPI
    
    @IBOutlet weak var usernameTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        navigationController?.navigationBar.barTintColor = UIColor(red: 181.0 / 255.0, green: 87.0 / 255.0, blue: 78.0 / 255.0, alpha: 1.0)
        navigationController?.navigationBar.tintColor = UIColor.whiteColor()
        navigationController?.navigationBar.barStyle = .Black
        
    }
    
    @IBAction func createUser(sender: UIButton) {
        
        let username = usernameTextField.text as String
        
        api.userNameIsValid(username,completion:{ (success: Bool) -> Void in
            if (success) {
                // Username available: create new user
                // Create a user by doing a POST request to /sessions with parameters of a user object(name, email, FB id, username)
                var userRequest : FBRequest = FBRequest.requestForMe()
                userRequest.startWithCompletionHandler{(connection: FBRequestConnection!, result: AnyObject!, error: NSError!) -> Void in
                    
                    if (error == nil) {
                        let userName = result["name"] as! String
                        let userID = result["id"] as! String
                        let userEmail = result["email"] as! String
                        
                        self.api.getSession({ (user: User) -> Void in
                            let user = [
                                "email": userEmail,
                                "name": userName,
                                "username": username,
                                "fbid": userID
                            ]
                        })
                        
                    } else {
                        println("Error")
                    }
                }
                
            } else {
                // Username already taken (prompt user with error alert in UsernameVC)
                var errorAlert = UIAlertController(title: "Sorry!", message: "Username is taken.", preferredStyle: UIAlertControllerStyle.Alert)
                errorAlert.addAction(UIAlertAction(title: "Try again", style: UIAlertActionStyle.Default, handler: nil))
                self.presentViewController(errorAlert, animated: true, completion: nil)
                self.clearTextField()
            }
        })
        
    }
    
    func clearTextField() {
        usernameTextField.text = ""
    }
    
    override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: NSBundle?) {
        super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
        // Custom initialization
        println("username view controller")
    }
    
    required init(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
}
