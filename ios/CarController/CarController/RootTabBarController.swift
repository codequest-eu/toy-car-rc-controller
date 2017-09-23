//
//  ViewController.swift
//  CarController
//
//  Created by mdziubich on 10/09/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import UIKit

class RootTabBarController: UITabBarController {

    override func viewDidLoad() {
        super.viewDidLoad()
        setupTabBarAppearance()
        setupTabBarControllers()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    private func setupTabBarAppearance() {
        tabBar.backgroundColor = UIColor.black
        tabBar.barTintColor = UIColor.black
        tabBar.isTranslucent = false
    }
    
    private func setupTabBarControllers() {
        let actionTabBar = UITabBarItem(title: "ACTIONS", image: #imageLiteral(resourceName: "actions"), selectedImage: nil)
        let listTabBar = UITabBarItem(title: "RECORDING LIST", image: #imageLiteral(resourceName: "record list"), selectedImage: nil)
        
        let actionsViewController = storyboard!.instantiateViewController(withIdentifier: "ActionViewController")
        actionsViewController.tabBarItem = actionTabBar
        
        let recordingListViewController = storyboard!.instantiateViewController(withIdentifier: "RecordingListViewController")
        recordingListViewController.tabBarItem = listTabBar
        
        viewControllers = [actionsViewController, recordingListViewController]
    }
}
