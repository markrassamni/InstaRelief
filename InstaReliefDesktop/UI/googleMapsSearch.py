import googlemaps
from googleplaces import GooglePlaces, types, lang
from geopy.distance import vincenty, great_circle
from googlemaps import convert
import math
import pyrebase
import requests

config = {
  "apiKey": "AIzaSyAFjbldaX_ZJw_yOLahlYJNFtlBbxP8hTg",
  "authDomain": "ngcode-9f40c.firebaseapp.com",
  "databaseURL": "https://ngcode-9f40c.firebaseio.com",
  "storageBucket": "ngcode-9f40c.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

gmaps = googlemaps.Client(key='AIzaSyBgFJr6eJK7QgPRMX205_Cv2QsCiKZZUnI')

def get_locals(lat, lng):

    YOUR_API_KEY = 'AIzaSyBgFJr6eJK7QgPRMX205_Cv2QsCiKZZUnI'
    base = "http://maps.googleapis.com/maps/api/geocode/json?"

    latlng = {}
    latlng['lat'] = lat
    latlng['lng'] = lng

    destination = gmaps.reverse_geocode(latlng)
    street_name = destination[0]['address_components'][1]['long_name']
    print(street_name)


    google_places = GooglePlaces(YOUR_API_KEY)
    stores = [types.TYPE_HARDWARE_STORE,
              types.TYPE_CONVENIENCE_STORE,
              types.TYPE_GROCERY_OR_SUPERMARKET]  # types.TYPE_SHOPPING_MALL,

    store_result = google_places.nearby_search(lat_lng=latlng,
                                               radius=5000, types=stores)

    gas_result = google_places.nearby_search(lat_lng=latlng, name='gas',
                                             radius=5000, types=types.TYPE_GAS_STATION)

    police_result = google_places.nearby_search(lat_lng=latlng, name='police',
                                                radius=5000, types=types.TYPE_POLICE)

    fireStation_result = google_places.nearby_search(lat_lng=latlng, name='fire dept. station',
                                                     radius=5000, types=types.TYPE_FIRE_STATION)


    for place in store_result.places:
        # Returned places from a query are place summaries.
        geo = place.geo_location
        geo_lat = float(geo['lat'])
        geo_lng = float(geo['lng'])
        geo = (geo_lat, geo_lng)
        data ={'name': place.name, 'geo': geo}
        print(place.geo_location)
        db.child(street_name).child("locals").child('stores').push(data)

    for place in gas_result.places:
        # Returned places from a query are place summaries.
        geo = place.geo_location
        geo_lat = float(geo['lat'])
        geo_lng = float(geo['lng'])
        geo = (geo_lat, geo_lng)
        data = {'name': place.name, 'geo': geo}
        print(place.geo_location)
        db.child(street_name).child("locals").child('gas').push(data)

    for place in police_result.places:
        # Returned places from a query are place summaries.
        geo = place.geo_location
        geo_lat = float(geo['lat'])
        geo_lng = float(geo['lng'])
        geo = (geo_lat, geo_lng)
        data = {'name': place.name, 'geo': geo}
        print(place.geo_location)
        db.child(street_name).child("locals").child('police').push(data)

    for place in fireStation_result.places:
        # Returned places from a query are place summaries.
        geo = place.geo_location
        geo_lat = float(geo['lat'])
        geo_lng = float(geo['lng'])
        geo = (geo_lat, geo_lng)
        data = {'name': place.name, 'geo': geo}
        print(place.geo_location)
        db.child(street_name).child("locals").child('fire stations').push(data)

    if store_result.has_attributions:
        print(store_result.html_attributions)

    for place in store_result.places:
        # Returned places from a query are place summaries.
        print(place.name)
        print(place.geo_location)
        print(place.place_id + "\n")

    geo1 = store_result.places[0].geo_location
    geo1_lat = float(geo1['lat'])
    geo1_lng = float(geo1['lng'])

    geo2 = store_result.places[1].geo_location
    geo2_lat = float(geo2['lat'])
    geo2_lng = float(geo2['lng'])

    radius = 6371 * 1000
    dlat = math.radians(geo2_lat - geo1_lat)
    dlon = math.radians(geo2_lng - geo1_lng)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(geo1_lat)) \
                                                  * math.cos(math.radians(geo2_lat)) * math.sin(dlon / 2) * math.sin(
        dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    if d < 4000:
        print("gucci $$$$")

    return street_name

if __name__ == "__main__":
    loc = get_locals(33.893229, -118.374267)
    print("hi")
