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
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
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
        
//        let center = CLLocationCoordinate2D(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
        
        
//        let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01))
        
//        self.map.setRegion(region, animated: true)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
         print("Error: " + error.localizedDescription)
    }
    
    func reportDanger(danger: String){
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
            errorAlert.show(self, sender: nil)
            self.locationManager.requestLocation()
        }
        
    }
    
    func requestReport(){
        // send location and phone number
//        let phoneRef = ref.child("texts")
        if let city = currentCity {
//            phoneRef.observeSingleEvent(of: .value, with: { snapshot in
//                print(snapshot.childrenCount) // I got the expected number of items
//                let enumerator = snapshot.children
//                while let rest = enumerator.nextObject() as? DataSnapshot {
//                    print(rest.value)
//                }
//            })
//            let link = "http://www.apple.com/euro/ios/ios8/a/generic/images/og.png"
//            guard let url = URL(string: link) else { return }
//            getDataFromUrl(url: url, completion: { (data: Data?, response: URLResponse?, error: Error?) in
//
//            })
            
            if let url = URL(string: "http://www.apple.com/euro/ios/ios8/a/generic/images/og.png") {
//                imageView.contentMode = .scaleAspectFit
                downloadImage(url: url)
            }
            
        } else {
            let errorAlert = UIAlertController(title: "Current Location Unavailable", message: "Your device is not able to send your current location. Try again later.", preferredStyle: .alert)
            errorAlert.show(self, sender: nil)
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

    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
