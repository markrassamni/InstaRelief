//
//  OfflineVC.swift
//  InstaRelief
//
//  Created by Mark Rassamni on 10/13/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import UIKit

class OfflineVC: UIViewController, UITextFieldDelegate, UIPickerViewDelegate, UIPickerViewDataSource {
    
    
    @IBOutlet weak var crossStreetsTxt: UITextField!
    @IBOutlet weak var cityTxt: UITextField!
    @IBOutlet weak var stateTxt: UITextField!
    @IBOutlet weak var countryTxt: UITextField!
    @IBOutlet weak var dangerTxt: UITextField!
    @IBOutlet weak var dangerView: UIView!
    @IBOutlet weak var dangerPicker: UIPickerView!
    @IBOutlet weak var messageSentImageView: UIImageView!
    
    
    var pickerDataSource = ["Fire", "Flood", "Zombie", "Hurricane", "Tornado"];
    let messageComposer = MessageComposer()
    
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
        crossStreetsTxt.delegate = self
    }
    
    func textFieldShouldBeginEditing(_ textField: UITextField) -> Bool {
        if textField == dangerTxt {
            dangerTxt.isHidden = true
            dangerView.isHidden = false
            return false
        }
        return true
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return pickerDataSource.count
    }
    
    func pickerView(pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String! {
        return pickerDataSource[row]
    }
    
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        dangerView.isHidden = true
        dangerTxt.isHidden = false
        dangerTxt.text = "\(pickerDataSource[row])"
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return "\(pickerDataSource[row])"
    }
    
    @IBAction func sendPressed(_ sender: Any) {
         //Make sure the device can send text messages
                if (messageComposer.canSendText()) {
                    // Obtain a configured MFMessageComposeViewController
                    if let streets = crossStreetsTxt.text {
                        if let city = cityTxt.text {
                            if let state = stateTxt.text {
                                if let country = countryTxt.text {
                                    if let danger = dangerTxt.text {
                                        let text = "\(streets)//\(city)//\(state)//\(country)//\(danger)"
                                        let messageComposeVC = messageComposer.configureTextMessage(text: text)
                                        present(messageComposeVC, animated: true, completion: nil)
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
    
    func sentSuccessfully(){
        print("CAlled")
        UIViewPropertyAnimator(duration: 0.5, curve: .easeOut, animations: {
            self.messageSentImageView.alpha = 1.0
        }).startAnimation()
        
//        let when = DispatchTime.now() + 0.5
//        DispatchQueue.main.asyncAfter(deadline: when) {
//            UIViewPropertyAnimator(duration: 0.5, curve: .easeIn, animations: {
//                self.messageSentImageView.alpha = 0.0
//            }).startAnimation()
//        }
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        print("Should return")
        textField.resignFirstResponder()
        return true
    }
    
    
}

