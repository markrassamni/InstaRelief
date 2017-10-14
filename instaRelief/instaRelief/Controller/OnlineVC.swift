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
import GoogleMaps

class OnlineVC: UIViewController, CLLocationManagerDelegate, UIPickerViewDelegate, UIPickerViewDataSource {
    
    let locationManager = CLLocationManager()
    var ref: DatabaseReference!
    var currentLocation: CLLocation?
    var currentCity: String?
    fileprivate var dangerToReport: String!
    
    @IBOutlet weak var reportButton: UIButton!
    @IBOutlet weak var requestButton: UIButton!
    @IBOutlet weak var dangerView: UIView!
    @IBOutlet weak var dangerPicker: UIPickerView!
    @IBOutlet weak var successImage: UIImageView!
    @IBOutlet weak var dangerImageView: UIImageView!
    @IBOutlet weak var imageSpinner: UIActivityIndicatorView!
    @IBOutlet weak var timeUpdatedLbl: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestAlwaysAuthorization()
        ref = Database.database().reference()
        dangerPicker.delegate = self
        dangerPicker.dataSource = self
        imageSpinner.isHidden = true
    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedAlways || status == .authorizedWhenInUse{
            locationManager.startUpdatingLocation()
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        // save current location coordinates and city
        currentLocation = locations.last! as CLLocation
        let geoCoder = CLGeocoder()
        geoCoder.reverseGeocodeLocation(self.currentLocation!) { placemarks, error in
            if let e = error {
                print("Error getting city: \(e)")
            } else {
                if let placeArray = placemarks as? [CLPlacemark] {
                    var placeMark: CLPlacemark!
                    placeMark = placeArray[0]
                    guard let address = placeMark.addressDictionary as? [String:Any] else {
                        return
                    }
                    if let city = address["City"] as? String{
                        self.currentCity = city
                    }
                }
            }
            
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
         print("Error: " + error.localizedDescription)
    }
    
    func reportDanger(danger: String){
        // user reports danger in his location
        if let location = currentLocation, let city = currentCity {
            let uuid = UIDevice.current.identifierForVendor!.uuidString
            let date = Date()
            let calendar = Calendar.current
            let month = calendar.component(.month, from: date)
            let day = calendar.component(.day, from: date)
            let hour = calendar.component(.hour, from: date)
            let minutes = calendar.component(.minute, from: date)
            let seconds = calendar.component(.second, from: date)
            let dateChild = "\(month) \(day) \(hour):\(minutes):\(seconds)"
            // fill all child objects in database
            self.ref.child("appUsers").child(uuid).child(dateChild).child("city").setValue(city) { (error, ref) -> Void in
                if error == nil {
                    self.ref.child("appUsers").child(uuid).child(dateChild).child("latitude").setValue(location.coordinate.latitude) { (error, ref) -> Void in
                        if error == nil {
                            self.ref.child("appUsers").child(uuid).child(dateChild).child("longitude").setValue(location.coordinate.longitude) { (error, ref) -> Void in
                                if error == nil {
                                    self.ref.child("appUsers").child(uuid).child(dateChild).child("danger").setValue(danger) { (error, ref) -> Void in
                                        if error == nil {
                                            self.successImage.alpha = 0.0
                                            UIViewPropertyAnimator(duration: 0.7, curve: .easeOut, animations: {
                                                self.successImage.isHidden = false
                                                self.successImage.alpha = 1.0
                                            }).startAnimation()
                                            let when = DispatchTime.now() + 0.7
                                            DispatchQueue.main.asyncAfter(deadline: when) {
                                                UIViewPropertyAnimator(duration: 0.7, curve: .easeOut, animations: {
                                                    self.successImage.alpha = 0.0
                                                }).startAnimation()
                                                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 0.7){
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
                }
            }
        }
        else {
            let errorAlert = UIAlertController(title: "Current Location Unavailable", message: "Your device is not able to send your current location. Try again or send as SMS", preferredStyle: .alert)
            let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .cancel) { action -> Void in
                errorAlert.dismiss(animated: true, completion: nil)
            }
            errorAlert.addAction(cancelAction)
            self.present(errorAlert, animated: true, completion: nil)
            self.locationManager.requestLocation()
        }
        
    }
    
    func requestReport(){
        // request danger information in current city
        if let city = currentCity {
            let cityRef = ref.child("Images")
            cityRef.observeSingleEvent(of: .value, with: { snapshot in
                let enumerator = snapshot.children
                var foundCity = false
                while let rest = enumerator.nextObject() as? DataSnapshot {
                    if rest.key == city{
                        foundCity = true
                        let urlRef = cityRef.child(rest.key)
                        urlRef.observeSingleEvent(of: .value, with: { snapshot in
                            let urlEnum = snapshot.children
                            while let restURL = urlEnum.nextObject() as? DataSnapshot {
                                // get image and time image was posted
                                if restURL.key == "url" {
                                    if let url = restURL.value as? String{
                                        if let urlAsString = URL(string: url){
                                            self.downloadImage(url: urlAsString)
                                        }
                                    }
                                } else if restURL.key == "updateTime" {
                                    if let time = restURL.value as? String {
                                        self.timeUpdatedLbl.text = "Updated: \(time)"
                                        self.timeUpdatedLbl.isHidden = false
                                    }
                                }
                            }
                        })
                    }
                }
                if !foundCity {
                    let errorAlert = UIAlertController(title: "No Danger Available", message: "Could not find any danger in \(city)", preferredStyle: .alert)
                    let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .cancel) { action -> Void in
                        errorAlert.dismiss(animated: true, completion: nil)
                    }
                    errorAlert.addAction(cancelAction)
                    self.present(errorAlert, animated: true, completion: nil)
                }
            })
        } else {
            let errorAlert = UIAlertController(title: "Current Location Unavailable", message: "Your device is not able to send your current location. Try again later.", preferredStyle: .alert)
            let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .cancel) { action -> Void in
                errorAlert.dismiss(animated: true, completion: nil)
            }
            errorAlert.addAction(cancelAction)
            self.present(errorAlert, animated: true, completion: nil)
            self.locationManager.requestLocation()
        }
    }
    
    func downloadImage(url: URL) {
        // Download Started
        imageSpinner.isHidden = false
        imageSpinner.startAnimating()
        getDataFromUrl(url: url) { data, response, error in
            guard let data = data, error == nil else { return }
            print(response?.suggestedFilename ?? url.lastPathComponent)
            // Download finished
            DispatchQueue.main.async() {
                self.dangerImageView.image = UIImage(data: data)
                self.dangerImageView.isHidden = false
                self.requestButton.isHidden = true
                self.reportButton.isHidden = true
                self.imageSpinner.stopAnimating()
                self.imageSpinner.isHidden = true
            }
        }
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        super.touchesBegan(touches, with: event)
        dangerImageView.isHidden = true
        reportButton.isHidden = false
        requestButton.isHidden = false
        timeUpdatedLbl.isHidden = true
        dangerView.isHidden = true
    }
    
    
    
    func getDataFromUrl(url: URL, completion: @escaping (Data?, URLResponse?, Error?) -> ()) {
        URLSession.shared.dataTask(with: url) { data, response, error in
            completion(data, response, error)
            }.resume()
    }
    
    @IBAction func reportPressed(_ sender: Any) {
        dangerView.isHidden = false
        reportButton.isHidden = true
        requestButton.isHidden = true
    }
    
    @IBAction func requestPressed(_ sender: Any) {
        requestReport()
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
    
    
    @IBAction func smsPressed(_ sender: Any) {
        performSegue(withIdentifier: "OnlineToOffline", sender: nil)
    }


}
