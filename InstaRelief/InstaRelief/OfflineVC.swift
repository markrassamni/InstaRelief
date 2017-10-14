//
//  OfflineVC.swift
//  InstaRelief
//
//  Created by Mark Rassamni on 10/13/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import UIKit

class OfflineVC: UIViewController, UITextFieldDelegate {
    
    @IBOutlet weak var crossStreetsTxt: UITextField!
    @IBOutlet weak var cityTxt: UITextField!
    @IBOutlet weak var stateTxt: UITextField!
    @IBOutlet weak var countryTxt: UITextField!
    @IBOutlet weak var dangerTxt: UITextField!
    
    @IBOutlet weak var dangerView: UIView!
    @IBOutlet weak var dangerPicker: UIPickerView!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        dangerView.isHidden = true
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func textFieldDidBeginEditing(_ textField: UITextField) {
        if textField == dangerTxt {
            print("DANGER")
            dangerView.isHidden = false
            dangerTxt.isHidden = true
        }
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        if textField == dangerTxt {
            dangerView.isHidden = true
            dangerTxt.isHidden = false
        }
    }
    
    @IBAction func sendPressed(_ sender: Any) {
        
    }
    
    
}

