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
        
        fixFrameOfTabBarItemsImageViews()
    }
    
    fileprivate func fixFrameOfTabBarItemsImageViews() {
        tabBar.subviews.forEach {
            let tabBarItemImageView = $0.subviews.flatMap { $0 as? UIImageView }.first
            setupTabBarImage(tabBarItemImageView)
        }
    }
    
    fileprivate func setupTabBarImage(_ imageView: UIImageView?) {
        guard let imageView = imageView else { return }
        
        let frame = imageView.frame
        imageView.frame = CGRect(x: frame.origin.x, y: frame.origin.y, width: 25, height: 25)
        imageView.contentMode = .scaleToFill
    }
}

//MARK: UITabBarDelegate

extension RootTabBarController {
    
    override func tabBar(_ tabBar: UITabBar, didSelect item: UITabBarItem)  {
        fixFrameOfTabBarItemsImageViews()
    }
}
