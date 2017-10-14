//
//  LoadingVC.swift
//  instaRelief
//
//  Created by Mark Rassamni on 10/14/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import UIKit

class LoadingVC: UIViewController {
    
    // Decide if user has data or should load the SMS page
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        let when = DispatchTime.now() + 0.5
        DispatchQueue.main.asyncAfter(deadline: when) {
            if isInternetAvailable(){
                self.performSegue(withIdentifier: "OnlineVC", sender: nil)
            } else {
                DispatchQueue.main.asyncAfter(deadline: when + 1){
                    if isInternetAvailable(){
                        self.performSegue(withIdentifier: "OnlineVC", sender: nil)
                    } else {
                        self.performSegue(withIdentifier: "OfflineVC", sender: nil)
                    }
                }
            }
        }
    }
}
