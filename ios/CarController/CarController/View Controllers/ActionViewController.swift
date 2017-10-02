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
    @IBOutlet weak var actionContainerView: UIView!
    
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var statusContainerView: UIView!
    
    enum ActionStatus {
        case idle,
            freeRide,
            collectingDataFromCamera,
            recordingTrackWithoutCamera,
            autonomusMode,
            playingSavedTrack
    
        var statusTitle: String {
            switch self {
            case .idle: return "IDLE"
            case .freeRide: return "Free Ride"
            case .collectingDataFromCamera: return "Collecting Data From Camera"
            case .recordingTrackWithoutCamera: return "Record Track Without Camera"
            case .autonomusMode: return "Autonomus Ride"
            case .playingSavedTrack: return "Playing Saved Track"
            }
        }
    }
    
    var status: ActionStatus = .idle {
        didSet {
            habdleActionChanges()
        }
    }
    
    //MARK: View life cycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        status = .idle
    }
    
    //MARK: Actions

    @IBAction func run(_ sender: Any) {
        switch status {
        case .idle:
            presentModeChooser()
            status = .autonomusMode
        default:
            status = .idle
        }
    }
    
    func presentModeChooser() {
        
    }
    

    //MARK: Private functions
    
    private func habdleActionChanges() {
        switch status {
        case .idle:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button"))])
        default:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "stop-button"))])
        }

        statusLabel.text = status.statusTitle
    }
    
    private func updateButtonsImage(for buttonsArray: [(button: UIButton, image: UIImage)]) {
        buttonsArray.forEach {
            $0.button.setImage($0.image, for: .normal)
        }
    }
    
    private func drawBorder(_ view: UIView) {
        view.layer.borderColor = UIColor.black.cgColor
        view.layer.borderWidth = 1
    }
    
    private func setupRecordingButtons(withAlpha alpha: CGFloat) {
    }
    
    private func animateRecording() {
//        UIView.animate(withDuration: 0.7, delay: 0, options: [.autoreverse, .repeat], animations: {
//            self.activeRecordActionView.alpha = 0
//        }, completion: nil)
    }
    
    func removeRecordingAnimation() {
//        activeRecordActionView.layer.removeAllAnimations()
//        activeRecordActionView.alpha = 1
//        view.layoutIfNeeded()
    }
}
