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

class OnlineVC: UIViewController, CLLocationManagerDelegate {
    
    
    
    
    let locationManager = CLLocationManager()
    let GOOGLE_API_KEY = "AIzaSyButIsDYJy_Xau-VmvewsvH4e7H78KJF0s"
    var ref: DatabaseReference!
    var currentLocation: CLLocation?
    
    
    @IBOutlet weak var reportButton: UIButton!
    @IBOutlet weak var requestButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.requestAlwaysAuthorization()
        ref = Database.database().reference()
    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedAlways || status == .authorizedWhenInUse{
            locationManager.startUpdatingLocation()
        }
    }
    
//    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
//        CLGeocoder().reverseGeocodeLocation(manager.location!, completionHandler: {(placemarks, error)->Void in
//
//            if (error != nil) {
//                print("Error: " + error!.localizedDescription)
//                return
//            }
//
//            if placemarks!.count > 0 {
//                let pm = placemarks![0] as CLPlacemark
//                self.displayLocationInfo(placemark: pm)
//            } else {
//                print("Error with the data.")
//            }
//        })
//    }
//
//    func displayLocationInfo(placemark: CLPlacemark) {
//
//        self.locationManager.stopUpdatingLocation()
//        print(placemark.locality)
//        print(placemark.postalCode)
//        print(placemark.administrativeArea)
//        print(placemark.country)
//
//    }
    
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
            let uuid = UIDevice.current.identifierForVendor!.uuidString
            let date = Date()
            let calendar = Calendar.current
            let month = calendar.component(.month, from: date)
            let day = calendar.component(.day, from: date)
            let hour = calendar.component(.hour, from: date)
            let minutes = calendar.component(.minute, from: date)
            let seconds = calendar.component(.second, from: date)
            let dateChild = "\(month) \(day) \(hour):\(minutes):\(seconds)"
            self.ref.child("appUsers").child(uuid).child(dateChild).setValue(["latitude": location.coordinate.latitude])
            self.ref.child("appUsers").child(uuid).child(dateChild).setValue(["longitude": location.coordinate.longitude])
            self.ref.child("appUsers").child(uuid).child(dateChild).setValue(["danger": danger])
        }
        else {
            // TODO: alert error no location available, try again later
            self.locationManager.requestLocation()
        }
        
    }
    
    func requestReport(){
        // send location and phone number
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
