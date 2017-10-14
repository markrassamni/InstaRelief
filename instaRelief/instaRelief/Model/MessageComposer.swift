//
//  MessageComposer.swift
//  instaRelief
//
//  Created by Mark Rassamni on 10/13/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import Foundation
import MessageUI


class MessageComposer: NSObject, MFMessageComposeViewControllerDelegate {
    
    var offlineVC: OfflineVC?
    
    // A wrapper function to indicate whether or not a text message can be sent from the user's device
    func canSendText() -> Bool {
        return MFMessageComposeViewController.canSendText()
    }
    
    func configureTextMessage(text: String, offlineVC: OfflineVC) -> MFMessageComposeViewController{
        let messageComposeVC = MFMessageComposeViewController()
        messageComposeVC.messageComposeDelegate = self
        messageComposeVC.recipients = textMessageRecipients
        messageComposeVC.body = text
        self.offlineVC = offlineVC
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
