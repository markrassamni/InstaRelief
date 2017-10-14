//
//  OnlineVC.swift
//  instaRelief
//
//  Created by Mark Rassamni on 10/14/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import UIKit
import CoreLocation
import Firebase

class OnlineVC: UIViewController, CLLocationManagerDelegate, UIPickerViewDelegate, UIPickerViewDataSource {
    
    
    
    
    let locationManager = CLLocationManager()
    var ref: DatabaseReference!
    var currentLocation: CLLocation?
    fileprivate var dangerToReport: String!
    
    
    
    @IBOutlet weak var reportButton: UIButton!
    @IBOutlet weak var requestButton: UIButton!
    @IBOutlet weak var dangerView: UIView!
    @IBOutlet weak var dangerPicker: UIPickerView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.requestAlwaysAuthorization()
        ref = Database.database().reference()
        dangerPicker.delegate = self
        dangerPicker.dataSource = self
    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedAlways || status == .authorizedWhenInUse{
            locationManager.startUpdatingLocation()
        }
    }
    
    
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
//        let location = locations.last! as CLLocation
        currentLocation = locations.last! as CLLocation
        
//        let center = CLLocationCoordinate2D(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
        
        
//        let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01))
        
//        self.map.setRegion(region, animated: true)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
         print("Error: " + error.localizedDescription)
    }
    
    func reportDanger(danger: String){
        if let location = currentLocation {
            print(location.coordinate.latitude)
            print(location.coordinate.longitude)
            let uuid = UIDevice.current.identifierForVendor!.uuidString
            let date = Date()
            let calendar = Calendar.current
            let month = calendar.component(.month, from: date)
            let day = calendar.component(.day, from: date)
            let hour = calendar.component(.hour, from: date)
            let minutes = calendar.component(.minute, from: date)
            let seconds = calendar.component(.second, from: date)
            let dateChild = "\(month) \(day) \(hour):\(minutes):\(seconds)"
            self.ref.child("appUsers").child(uuid).child(dateChild).child("latitude").setValue(location.coordinate.latitude) { (error, ref) -> Void in
                if error == nil {
                     self.ref.child("appUsers").child(uuid).child(dateChild).child("longitude").setValue(location.coordinate.longitude) { (error, ref) -> Void in
                        if error == nil {
                            self.ref.child("appUsers").child(uuid).child(dateChild).child("danger").setValue(danger) { (error, ref) -> Void in
                                if error == nil {
                                    let storyboard = UIStoryboard(name: "Main", bundle: nil)
                                    let controller = storyboard.instantiateViewController(withIdentifier: "SuccessVC")
                                    controller.modalPresentationStyle = .overCurrentContext
                                    self.present(controller, animated: true, completion: nil)
                                    let when = DispatchTime.now() + 1
                                    DispatchQueue.main.asyncAfter(deadline: when) {
                                        controller.dismiss(animated: true, completion: nil)
                                        self.reportButton.isHidden = false
                                        self.requestButton.isHidden = false
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
        }
        else {
            // TODO: alert error no location available, try again later
            self.locationManager.requestLocation()
        }
        
    }
    
    func requestReport(){
        // send location and phone number
    }
    
    
    @IBAction func reportPressed(_ sender: Any) {
        dangerView.isHidden = false
        reportButton.isHidden = true
        requestButton.isHidden = true
    }
    
    @IBAction func requestPressed(_ sender: Any) {
        
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
        dangerToReport = dangerSources[row]
    }
    
    @IBAction func selectPickerItem(_ sender: Any) {
        dangerView.isHidden = true
        if let danger = dangerToReport {
            reportDanger(danger: danger)
        }
    }
    
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return "\(dangerSources[row])"
    }
    


    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
