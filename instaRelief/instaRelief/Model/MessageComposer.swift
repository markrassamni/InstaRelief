//
//  MessageComposer.swift
//  instaRelief
//
//  Created by Mark Rassamni on 10/13/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import Foundation
import MessageUI

let textMessageRecipients = ["1-619-304-5612"] 

class MessageComposer: NSObject, MFMessageComposeViewControllerDelegate {
    
    var offlineVC: OfflineVC?
    
    // A wrapper function to indicate whether or not a text message can be sent from the user's device
    func canSendText() -> Bool {
        return MFMessageComposeViewController.canSendText()
    }
    
    // Configures and returns a MFMessageComposeViewController instance
    func configuredMessageComposeViewController() -> MFMessageComposeViewController {
        let messageComposeVC = MFMessageComposeViewController()
        messageComposeVC.messageComposeDelegate = self  //  Make sure to set this property to self, so that the controller can be dismissed!
        messageComposeVC.recipients = textMessageRecipients
        messageComposeVC.body = "Hey friend - Just sending a text message in-app using Swift!"
        return messageComposeVC
    }
    
    func configureTextMessage(text: String) -> MFMessageComposeViewController{
        let messageComposeVC = MFMessageComposeViewController()
        messageComposeVC.messageComposeDelegate = self
        messageComposeVC.recipients = textMessageRecipients
        messageComposeVC.body = text
        if let wd = UIApplication.shared.delegate?.window{
            let vc = wd!.rootViewController
            if vc is OfflineVC {
                offlineVC = vc as? OfflineVC
            }
        }
        return messageComposeVC
    }
    
    // MFMessageComposeViewControllerDelegate callback - dismisses the view controller when the user is finished with it
    func messageComposeViewController(_ controller: MFMessageComposeViewController, didFinishWith result: MessageComposeResult) {
        controller.dismiss(animated: true, completion: {
            if result == .sent {
                self.offlineVC?.sentSuccessfully()
            }
        })
    }
}
