from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import json
import pyrebase
import re

# User Credentials
access_token = "919017548452003840-OoV9muwD1Ct4Vb7xpbv80WhGQKDzWUJ"
access_token_secret = "fmehS5sHuV9neS6E3CwfznHMI27NNbxbQSfYGibwiQW2t"
consumer_key = "Mv2QN24elvdC5YbqVlSeq9Iui"
consumer_secret = "tGZjOHxg9e2IHpxFENecxexXArJJI3UNmuLr7VATbFaCWdRfmf"

config = {
  "apiKey": "AIzaSyAFjbldaX_ZJw_yOLahlYJNFtlBbxP8hTg",
  "authDomain": "ngcode-9f40c.firebaseapp.com",
  "databaseURL": "https://ngcode-9f40c.firebaseio.com",
  "storageBucket": "ngcode-9f40c.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


class StdOutListener(StreamListener):
    numTweets = 0
    currentText = None
    currentLocation = None
    text_file = None

    def set_file(self, file):
        self.text_file = file

    def on_data(self, data):
        # write to text file
        print(data)
        text_file.write(data)
        text_file.flush()
        self.numTweets += 1
        time.sleep(0.1)
        data = json.loads(data)
        self.upload_data(data)
        return True

    def on_error(self, status):
        text_file.write(status)
        print(status)

    @staticmethod
    def upload_data(data):
        # save important information to variables
        tweet = data
        tweet_text = tweet['text']
        tweet_name = tweet['user']['name']
        tweet_screen_name = tweet['user']['screen_name']
        tweet_created_at = tweet['user']['created_at']
        tweet_coords = tweet['coordinates']
        # tweetMediaUrl = tweet[0]['entities']['media']['media_url_https']

        match = False
        if "danger" in tweet_text:
            match = True
        are_coords = False

        if tweet_coords is not None:
                are_coords = True
        if are_coords and match:
            data = {"text": tweet_text, "name": tweet_name, "screen_name": tweet_screen_name,
                    "coordinates": tweet_coords, "created_at": tweet_created_at}
            db.child("Danger Tweets").child(tweet_screen_name).child(tweet_created_at).push(data)
            print("Danger Tweet added")

        # upload variables to database
        data = {"text": tweet_text, "name": tweet_name, "screen_name": tweet_screen_name, "coordinates": tweet_coords, "created_at": tweet_created_at}
        db.child("Tweets").child(tweet_screen_name).child(tweet_created_at).push(data)
        print("Tweet added")

if __name__ == '__main__':
    def word_in_text(word, text):
        text = str(text)
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)

        if match:
            print("match")
            return True
        return False

    def upload_latest_tweets(name, number):
        status = api.user_timeline(screen_name=name, count=number)
        for tweet in status:
            listen.upload_data(tweet)

    text_file = open("CalFireFeed.txt", "w")
    time.sleep(1.0)
    listen = StdOutListener()
    listen.set_file(text_file)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listen)

    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    upload_latest_tweets("SanDiegoPD", 10)
    upload_latest_tweets("CALFIRES", 10)

    # listening for new tweets from specified users
    print("listening: ")
    stream.filter(follow=['876731042'], track=['#NGDemo', '#NorCalFires', '#SantaRosaFire', '#HurricaneOphelia'])  # 876731042 is kelly
    text_file.close()
