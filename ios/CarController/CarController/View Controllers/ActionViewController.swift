//
//  ActionViewController.swift
//  CarController
//
//  Created by mdziubich on 10/09/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import UIKit
import SVProgressHUD

class ActionViewController: UIViewController {
    
    @IBOutlet weak var runButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    @IBOutlet weak var actionContainerView: UIView!
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var statusContainerView: UIView!
    @IBOutlet weak var velocityLabel: UILabel!
    @IBOutlet weak var plusVelocityButton: UIButton!
    @IBOutlet weak var minusVelocityButton: UIButton!
    @IBOutlet weak var ipTextField: UITextField!
    
    var currentVelocity = 1536 {
        didSet {
            velocityLabel.text = "Velocity \(currentVelocity)"
        }
    }
    let defaultVelocityChangeValue = 1
    
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
        presentModeChooser()
    }
    
    @IBAction func stop(_ sender: Any) {
         perform(action: .stop)
    }
    
    @IBAction func increaseVelocity(_ sender: Any) {
        perform(action: .changeSpeed(currentVelocity + defaultVelocityChangeValue))
    }
    
    @IBAction func decreaseVelocity(_ sender: Any) {
        perform(action: .changeSpeed(currentVelocity - defaultVelocityChangeValue))
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
//        switch status {
//        case .stop, .idle:
//            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "play-button"))])
//        default:
//            updateButtonsImage(for: [(runButton, #imageLiteral(resourceName: "stop-button"))])
//        }
        statusLabel.text = status.statusTitle
    }
    /*
    private func updateButtonsImage(for buttonsArray: [(button: UIButton, image: UIImage)]) {
        buttonsArray.forEach {
            $0.button.setImage($0.image, for: .normal)
        }
    }*/
    
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
        SVProgressHUD.show()
        blockButtons(isActionPerforming: true)
        
        CarActionsAPIHelper().request(action: action) { (success, error) in
            SVProgressHUD.dismiss()
            self.blockButtons(isActionPerforming: false)
            
            guard let errorMsg = error, !success else {
                switch action {
                case .changeSpeed(let updatedSpeed):
                    self.currentVelocity = updatedSpeed
                default:
                    self.status = action
                }
                return
            }
            let alert = UIAlertController(title: "Error", message: errorMsg, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "Dismiss", style: .default, handler: nil))
            self.present(alert, animated: true, completion: nil)
        }
    }
    
    private func blockButtons(isActionPerforming: Bool) {
        runButton.isUserInteractionEnabled = !isActionPerforming
        plusVelocityButton.isUserInteractionEnabled = !isActionPerforming
        minusVelocityButton.isUserInteractionEnabled = !isActionPerforming
    }
}

extension ActionViewController: ActionPickerViewControllerDelegate {
    
    func actionPickerViewControllerDelegateDidSelect(action: ActionType) {
        perform(action: action)
    }
}
