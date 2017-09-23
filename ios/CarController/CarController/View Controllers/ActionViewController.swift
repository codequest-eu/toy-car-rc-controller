//
//  ActionViewController.swift
//  CarController
//
//  Created by mdziubich on 10/09/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import UIKit

class ActionViewController: UIViewController {
    
    @IBOutlet weak var runButton: UIButton!
    @IBOutlet weak var recordButton: UIButton!
    @IBOutlet weak var statusLabel: UILabel!
    
    enum ActionStatus {
        case idle, running, paused, recording
    }
    
    var status: ActionStatus = .idle {
        didSet {
            
        }
    }

    //MARK: View life cycle
    
    override func viewDidLoad() {
        super.viewDidLoad()

    }
    
    //MARK: Actions

    @IBAction func run(_ sender: Any) {
        switch status {
        case .idle:
            status = .running
        case .running:
            status = .paused
        case .paused:
            status = .running
        case .recording: return
        }
    }
    
    @IBAction func record(_ sender: Any) {
//        switch status {
//        case .idle:
//
//        case .running:
//
//        case .paused:
//
//        case .recording:
//
//        }
    }
    
    //MARK: Private functions
    
    private func updateButtonsState() {
        switch status {
        case .idle:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record"))])
        case .running:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "pause")), (recordButton, #imageLiteral(resourceName: "record"))])
        case .paused:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record"))])
        case .recording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record"))]) //todo: update recordButton
        }
    }
    
    private func updateButtonsImage(for buttonsArray: [(button: UIButton, image: UIImage)]) {
        buttonsArray.forEach {
            $0.button.setImage($0.image, for: .normal)
        }
    }
}
