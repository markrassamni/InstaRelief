//
//  OfflineVC.swift
//  InstaRelief
//
//  Created by Mark Rassamni on 10/13/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import UIKit

class OfflineVC: UIViewController, UITextFieldDelegate, UIPickerViewDelegate, UIPickerViewDataSource {
    
    
    @IBOutlet weak var addressText: UITextField!
    @IBOutlet weak var cityTxt: UITextField!
    @IBOutlet weak var stateTxt: UITextField!
    @IBOutlet weak var countryTxt: UITextField!
    @IBOutlet weak var dangerTxt: UITextField!
    @IBOutlet weak var dangerView: UIView!
    @IBOutlet weak var dangerPicker: UIPickerView!
    @IBOutlet weak var zipTxt: UITextField!
    @IBOutlet weak var groupSizeLbl: UILabel!
    @IBOutlet weak var groupStepper: UIStepper!
    @IBOutlet weak var groupStack: UIStackView!
    
    
    fileprivate var peopleInGroup = 1
    
    fileprivate let messageComposer = MessageComposer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        dangerView.isHidden = true
        dangerTxt.delegate = self
        dangerPicker.delegate = self
        dangerPicker.dataSource = self
        cityTxt.delegate = self
        stateTxt.delegate = self
        countryTxt.delegate = self
        addressText.delegate = self
    }
    
    func textFieldShouldBeginEditing(_ textField: UITextField) -> Bool {
        if textField == dangerTxt {
            dangerTxt.isHidden = true
            dangerView.isHidden = false
            groupStack.isHidden = true
            view.endEditing(true)
            return false
        }
        return true
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return dangerSources.count
    }
    
    func pickerView(pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String! {
        return dangerSources[row]
    }
    
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        dangerTxt.text = "\(dangerSources[row])"
    }
    
    @IBAction func selectPickerItem(_ sender: Any) {
        dangerView.isHidden = true
        dangerTxt.isHidden = false
        groupStack.isHidden = false
    }
    
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return "\(dangerSources[row])"
    }
    
    @IBAction func sendPressed(_ sender: Any) {
         //Make sure the device can send text messages
                if (messageComposer.canSendText()) {
                    // Obtain a configured MFMessageComposeViewController
                    if let streets = addressText.text {
                        if let city = cityTxt.text {
                            if let state = stateTxt.text {
                                if let country = countryTxt.text {
                                    if let danger = dangerTxt.text {
                                        if let zip = zipTxt.text {
                                            let text = "\(streets)//\(city)//\(state)//\(zip)//\(country)//\(peopleInGroup)//\(danger)"
                                            let messageComposeVC = messageComposer.configureTextMessage(text: text)
                                            present(messageComposeVC, animated: true, completion: nil)
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else {
                    // Let the user know if his/her device isn't able to send text messages
                    let errorAlert = UIAlertController(title: "Cannot Send Text Message", message: "Your device is not able to send text messages.", preferredStyle: .alert)
                    errorAlert.show(self, sender: nil)
                }
    }
    
    @IBAction func stepperValueChanged(_ sender: UIStepper) {
        peopleInGroup = Int(sender.value)
        groupSizeLbl.text = "People in group: \(peopleInGroup)"
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        view.endEditing(true)
        super.touchesBegan(touches, with: event)
    }
    
    
    
    
    func sentSuccessfully(){
        addressText.text = ""
        cityTxt.text = ""
        stateTxt.text = ""
        countryTxt.text = ""
        dangerTxt.text = ""
        zipTxt.text = ""
        peopleInGroup = 1
        groupSizeLbl.text = "People in group: \(peopleInGroup)"
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let controller = storyboard.instantiateViewController(withIdentifier: "SuccessVC")
        controller.modalPresentationStyle = .overCurrentContext
        self.present(controller, animated: true, completion: nil)
        let when = DispatchTime.now() + 1
        DispatchQueue.main.asyncAfter(deadline: when) {
            controller.dismiss(animated: true, completion: nil)
        }
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    
}

