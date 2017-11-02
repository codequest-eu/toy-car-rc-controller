//
//  ActionPickerViewController.swift
//  CarController
//
//  Created by mdziubich on 11/10/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import UIKit

protocol ActionPickerViewControllerDelegate: class {
    func actionPickerViewControllerDelegateDidSelect(action: ActionType)
}

class ActionPickerViewController: UIViewController {

    @IBOutlet weak var cancelButton: UIButton!
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var tableViewHeight: NSLayoutConstraint!
    
    fileprivate let allStatuses = ActionType.allValues
    private let singleCellHeight: CGFloat = 48.0
    weak var delegate: ActionPickerViewControllerDelegate?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.dataSource = self
        tableView.delegate = self
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "ActionPickerTableViewCellId")
    }

    override func viewWillLayoutSubviews() {
        super.viewWillLayoutSubviews()
        tableViewHeight.constant = singleCellHeight * CGFloat(allStatuses.count)
        
        drawBorder(on: tableView)
        drawBorder(on: titleLabel)
        drawBorder(on: cancelButton)
        
        let blurEffect = UIBlurEffect(style: .light)
        let blurEffectView = UIVisualEffectView(effect: blurEffect)
        blurEffectView.frame = view.bounds
        blurEffectView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.insertSubview(blurEffectView, at: 0)
    }
    
    @IBAction func cancel(_ sender: Any) {
        dismiss(animated: true, completion: nil)
    }
    
    private func drawBorder(on view: UIView) {
        view.layer.borderColor = UIColor.black.cgColor
        view.layer.borderWidth = 1
    }
}

extension ActionPickerViewController: UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return allStatuses.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ActionPickerTableViewCellId", for: indexPath)
        cell.textLabel?.text = allStatuses[indexPath.row].statusTitle
        return cell
    }
}

extension ActionPickerViewController: UITableViewDelegate {
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        print(allStatuses[indexPath.row])
        delegate?.actionPickerViewControllerDelegateDidSelect(action: allStatuses[indexPath.row])
        dismiss(animated: true, completion: nil)
    }
}
