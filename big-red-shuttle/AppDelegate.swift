//
//  AppDelegate.swift
//  big-red-shuttle
//
//  Created by Kevin Greer on 10/12/16.
//  Copyright © 2016 cuappdev. All rights reserved.
//

import UIKit
import GoogleMaps
import SwiftyJSON

enum FileReadingError : Error { case fileNotFound }

var appEnteredForeground: Bool = true

extension UINavigationController{
    override open func viewDidLoad() {
        navigationBar.titleTextAttributes = [NSForegroundColorAttributeName: UIColor.brsblack, NSFontAttributeName: UIFont(name: "HelveticaNeue-Medium" , size: 18.0)!]
        navigationBar.barTintColor = .brslightgrey
        navigationBar.isTranslucent = false
    }
}


@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate, UITabBarControllerDelegate {
    let tabBarController = UITabBarController()
    
    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        
        // Styling
        UIApplication.shared.statusBarStyle = .lightContent
        UINavigationBar.appearance().titleTextAttributes = [NSForegroundColorAttributeName : UIColor.navtitleblack,
                                                            NSFontAttributeName: UIFont(name: "SFUIText-Semibold", size: 16)!]
        
        // Set nudge count for stop popup view
        if UserDefaults.standard.value(forKey: "nudgeCount") as? Int == nil {
            UserDefaults.standard.setValue(0, forKey: "nudgeCount")
        }
        UserDefaults.standard.setValue(true, forKey: "didFireNudge")
        
        // Set up Google Maps Services
        let json = try! JSON(data: Data(contentsOf: Bundle.main.url(forResource: "config", withExtension: "json")!))
        GMSServices.provideAPIKey(json["google-maps"].stringValue)

        // Set up tab bar & VCs
        let navigationVC = StopsViewController()
        let emergencyVC = UINavigationController(rootViewController: EmergencyViewController())
        let scheduleVC = UINavigationController(rootViewController: ScheduleViewController())
        
        let navigationIcon = UITabBarItem(title: "Navigation", image: UIImage(named: "navigation"), selectedImage: UIImage(named: "navigation-s"))
        let scheduleIcon = UITabBarItem(title: "Schedule", image: UIImage(named: "schedule"), selectedImage: UIImage(named: "schedule-s"))
        let emergencyIcon = UITabBarItem(title: "Emergency", image: UIImage(named: "emergency"), selectedImage: UIImage(named: "emergency-s"))
        navigationVC.tabBarItem = navigationIcon
        scheduleVC.tabBarItem = scheduleIcon
        emergencyVC.tabBarItem = emergencyIcon
        
        tabBarController.viewControllers = [navigationVC,scheduleVC,emergencyVC]
        tabBarController.tabBar.tintColor = .brsred
        UITabBarItem.appearance().setTitleTextAttributes([NSForegroundColorAttributeName: UIColor.brsblack], for:.normal)
        UITabBarItem.appearance().setTitleTextAttributes([NSForegroundColorAttributeName: UIColor.brsred], for:.selected)
        tabBarController.tabBar.clipsToBounds = true
        tabBarController.tabBar.isTranslucent = false
        tabBarController.tabBar.barTintColor = .brslightgrey
        tabBarController.tabBar.layer.borderWidth = 0.5
        tabBarController.tabBar.layer.borderColor = UIColor.lightGray.cgColor
        tabBarController.delegate = self
        
        //Set up window
        window = UIWindow(frame: UIScreen.main.bounds)
        window!.makeKeyAndVisible()
        window?.rootViewController = tabBarController
        
        displayNoInternetAlert(vc: (window?.rootViewController)!)
        
        //Kickstart location services
//        _ = Location.shared

        return true
    }
    
    var hiddenTabCounter = 0
    
    func tabBarController(_ tabBarController: UITabBarController, didSelect viewController: UIViewController) {
        hiddenTabCounter = tabBarController.selectedIndex == 0 ? tabBarController.selectedIndex + 1 : 0
        
        if hiddenTabCounter == 5 {
            viewController.present(DriverViewController(), animated: true, completion: nil)
            hiddenTabCounter = 0
        }
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
        
        displayNoInternetAlert(vc: (window?.rootViewController)!)
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }
    
    // MARK: - Force Touch Shortcut
    
    @available(iOS 9.0, *)
    func application(_ application: UIApplication, performActionFor shortcutItem: UIApplicationShortcutItem, completionHandler: @escaping (Bool) -> Void) {
        let handleShortcutItem = self.handleShortcutItem(shortcutItem)
        completionHandler(handleShortcutItem)
    }
    
    enum ShortcutIdentifier: String {
        case Schedule
        case Emergency
        
        init?(fullType: String) {
            guard let last = fullType.components(separatedBy: ".").last else {return nil}
            self.init(rawValue: last)
        }
        
        var type: String {
            return Bundle.main.bundleIdentifier! + ".\(self.rawValue)"
        }
    }
    
    @available(iOS 9.0, *)
    func handleShortcutItem(_ shortcutItem: UIApplicationShortcutItem) -> Bool {
        guard ShortcutIdentifier(fullType: shortcutItem.type) != nil else { return false }
        guard let shortcutType = shortcutItem.type as String? else { return false }
        
        func handleShortCutForMenuIndex(_ index: Int) {
            tabBarController.selectedViewController = tabBarController.viewControllers?[index]
        }
        
        switch (shortcutType) {
        case ShortcutIdentifier.Schedule.type:
            handleShortCutForMenuIndex(1)
        case ShortcutIdentifier.Emergency.type:
            handleShortCutForMenuIndex(2)
        default:
            return false
        }
        return true
    }
}

