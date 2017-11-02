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
    
    var status: ActionType = .stop {
        didSet {
            switch status {
            case .changeSpeed:
                return
            default:
                handleActionChanges()
            }
        }
    }
    
    //MARK: View life cycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        status = .stop
    }
    
    //MARK: Actions

    @IBAction func run(_ sender: Any) {
        switch status {
        case .idle, .stop:
            presentModeChooser()
        case .freeRemoteRide:
            perform(action: .idle)
        case .autonomusMode:
            perform(action: .stop)
        default:
            return
        }
    }
    
    func presentModeChooser() {
        guard let actionPickerViewController = storyboard?.instantiateViewController(withIdentifier: "ActionPickerViewControllerId") as? ActionPickerViewController else {
            return
        }
        actionPickerViewController.delegate = self
        actionPickerViewController.modalPresentationStyle = .overFullScreen
        present(actionPickerViewController, animated: true, completion: nil)
    }
    

    //MARK: Private functions
    
    private func handleActionChanges() {
        switch status {
        case .stop:
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
    
    fileprivate func perform(action: ActionType) {
        CarActionsAPIHelper().request(action: action) { (success, error) in
            guard let errorMsg = error, !success else {
                self.status = action
                return
            }
            
            let alert = UIAlertController(title: "Error", message: errorMsg, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "Dismiss", style: .default, handler: nil))
            self.present(alert, animated: true, completion: nil)
        }
    }
}

extension ActionViewController: ActionPickerViewControllerDelegate {
    
    func actionPickerViewControllerDelegateDidSelect(action: ActionType) {
        perform(action: action)
    }
}
