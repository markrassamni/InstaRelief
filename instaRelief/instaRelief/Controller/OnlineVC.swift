//
//  OnlineVC.swift
//  instaRelief
//
//  Created by Mark Rassamni on 10/14/17.
//  Copyright © 2017 markrassamni. All rights reserved.
//

import UIKit
import CoreLocation

class OnlineVC: UIViewController, CLLocationManagerDelegate {
    
    let locationManager = CLLocationManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.requestAlwaysAuthorization()
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
        let location = locations.last! as CLLocation
        
        let center = CLLocationCoordinate2D(latitude: location.coordinate.latitude, longitude: location.coordinate.longitude)
        
//        let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01))
        
//        self.map.setRegion(region, animated: true)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
         print("Error: " + error.localizedDescription)
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
