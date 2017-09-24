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
    @IBOutlet weak var stopButton: UIButton!
    @IBOutlet weak var actionContainerView: UIView!
    
    @IBOutlet weak var recordButton: UIButton!
    @IBOutlet weak var recordPauseButton: UIButton!
    @IBOutlet weak var recordStopButton: UIButton!
    @IBOutlet weak var recordingContainerView: UIView!
    
    @IBOutlet weak var activeRecordBorderView: UIView!
    @IBOutlet weak var activeRecordActionView: UIView!
    
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var statusContainerView: UIView!
    
    enum ActionStatus {
        case idle,
            idleWhileRecording,
            idleWhilePausedRecording,
            running,
            runningWhileRecording,
            runningWhilePausedRecording,
            pausedRunning,
            pausedRunningWhileRecording,
            pausedRunningWhilePausedRecording
    
        var statusTitle: String {
            switch self {
            case .idle: return "IDLE (recording off)"
            case .idleWhileRecording: return "IDLE (recording on)"
            case .idleWhilePausedRecording: return "IDLE (recording paused)"
            case .running: return "RUNNING (recording off)"
            case .runningWhileRecording: return "RUNNING (recording on)"
            case .runningWhilePausedRecording: return "RUNNING (recording paused)"
            case .pausedRunning: return "PAUSED (recording off)"
            case .pausedRunningWhileRecording: return "PAUSED RUNNING (recording on)"
            case .pausedRunningWhilePausedRecording: return "RUNNING PAUSED (recording paused)"
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
        drawBorder(actionContainerView)
        drawBorder(recordingContainerView)
        drawBorder(statusContainerView)
        
        activeRecordBorderView.layer.cornerRadius = activeRecordBorderView.frame.height / 2
        activeRecordActionView.layer.cornerRadius = activeRecordActionView.frame.height / 2
        
        activeRecordBorderView.layer.borderColor = UIColor.red.cgColor
        activeRecordBorderView.layer.borderWidth = 3
        
        status = .idle
    }
    
    //MARK: Actions

    @IBAction func run(_ sender: Any) {
        switch status {
        case .idle:
            status = .running
        case .idleWhileRecording:
            status = .runningWhileRecording
        case .idleWhilePausedRecording:
            status = .runningWhilePausedRecording
        case .running:
            status = .pausedRunning
        case .runningWhileRecording:
            status = .pausedRunningWhileRecording
        case .runningWhilePausedRecording:
            status = .pausedRunningWhilePausedRecording
        case .pausedRunning:
            status = .running
        case .pausedRunningWhileRecording:
            status = .runningWhileRecording
        case .pausedRunningWhilePausedRecording:
            status = .runningWhilePausedRecording
        }
    }
    
    @IBAction func stopRunning(_ sender: Any) {
        switch status {
        case .idle,
             .idleWhileRecording,
             .idleWhilePausedRecording:
            return
        case .running,
             .pausedRunning:
            status = .idle
        case .runningWhileRecording,
             .pausedRunningWhileRecording:
            status = .idleWhileRecording
        case .runningWhilePausedRecording,
             .pausedRunningWhilePausedRecording:
            status = .idleWhilePausedRecording
        }
    }
    
    @IBAction func record(_ sender: Any) {
        switch status {
        case .idle:
            status = .idleWhileRecording
        case .idleWhileRecording,
             .idleWhilePausedRecording,
             .runningWhileRecording,
             .runningWhilePausedRecording,
             .pausedRunningWhileRecording,
             .pausedRunningWhilePausedRecording:
            return
        case .running:
            status = .runningWhileRecording
        case .pausedRunning:
            status = .pausedRunningWhileRecording
        }
        
        recordButton.alpha = 0
        activeRecordBorderView.alpha = 1
        animateRecording()
    }
    
    @IBAction func pauseRecording(_ sender: Any) {
        switch status {
        case .idle,
             .running,
             .pausedRunning:
            return
        case .idleWhileRecording:
            status = .idleWhilePausedRecording
            removeRecordingAnimation()
        case .idleWhilePausedRecording:
            animateRecording()
            status = .idleWhileRecording
        case .runningWhileRecording:
            removeRecordingAnimation()
            status = .runningWhilePausedRecording
        case .runningWhilePausedRecording:
            animateRecording()
            status = .runningWhileRecording
        case .pausedRunningWhileRecording:
            removeRecordingAnimation()
            status = .pausedRunningWhilePausedRecording
        case .pausedRunningWhilePausedRecording:
            animateRecording()
            status = .pausedRunningWhileRecording
        }
    }
    
    @IBAction func stopRecording(_ sender: Any) {
        //todo: Update
        status = .idle
        
        recordButton.alpha = 1
        activeRecordBorderView.alpha = 0
        removeRecordingAnimation()
    }
    
    @IBAction func saveRecording(_ sender: Any) {
        //todo: Update
        status = .idle
        
//        switch status {
//        case .idle:
//            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record"))])
//            stopButton.alpha = 0.2
//            recordPauseButton.alpha = 0.2
//            recordStopButton.alpha = 0.2
//        case .idleWhileRecording:
//
//        case .idleWhilePausedRecording:
//
//        case .running:
//
//        case .runningWhileRecording:
//
//        case .runningWhilePausedRecording:
//
//        case .pausedRunning:
//
//        case .pausedRunningWhileRecording:
//
//        case .pausedRunningWhilePausedRecording:
//
//        }
    }
    
    //MARK: Private functions
    
    private func habdleActionChanges() {
        switch status {
        case .idle:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "pause"))])
            stopButton.alpha = 0.2
            setupRecordingButtons(withAlpha: 0.2)
        case .idleWhileRecording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "pause"))])
            stopButton.alpha = 0.2
            setupRecordingButtons(withAlpha: 1)
        case .idleWhilePausedRecording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "play-button"))])
            stopButton.alpha = 0.2
        case .running:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "pause")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "pause"))])
            stopButton.alpha = 1
            setupRecordingButtons(withAlpha: 0.2)
        case .runningWhileRecording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "pause")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "pause"))])
            stopButton.alpha = 1
            setupRecordingButtons(withAlpha: 1)
        case .runningWhilePausedRecording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "pause")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "play-button"))])
            stopButton.alpha = 1
            setupRecordingButtons(withAlpha: 1)
        case .pausedRunning:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "pause"))])
            stopButton.alpha = 1
            setupRecordingButtons(withAlpha: 0.2)
        case .pausedRunningWhileRecording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "pause"))])
            stopButton.alpha = 1
            setupRecordingButtons(withAlpha: 1)
        case .pausedRunningWhilePausedRecording:
            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button")), (recordButton, #imageLiteral(resourceName: "record")), (recordPauseButton, #imageLiteral(resourceName: "play-button"))])
            stopButton.alpha = 1
            setupRecordingButtons(withAlpha: 1)
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
        recordPauseButton.alpha = alpha
        recordStopButton.alpha = alpha
    }
    
    private func animateRecording() {
        UIView.animate(withDuration: 0.7, delay: 0, options: [.autoreverse, .repeat], animations: {
            self.activeRecordActionView.alpha = 0
        }, completion: nil)
    }
    
    func removeRecordingAnimation() {
        activeRecordActionView.layer.removeAllAnimations()
        activeRecordActionView.alpha = 1
        view.layoutIfNeeded()
    }
}
