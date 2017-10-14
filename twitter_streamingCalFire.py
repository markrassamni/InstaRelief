from InstaReliefDesktop.UI.stream_tweets_ui import Form
from PyQt5.QtWidgets import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import json
import pyrebase
import re
import sys

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
    screen = None
    stream = None
    api = None

    def __init__(self, user_twitter_id, keywords):
        super(StdOutListener, self).__init__(None)
        self.text_file = open("CalFireFeed.txt", "w")

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth, self)

        self.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

        self.upload_latest_tweets("SanDiegoPD", 10)
        self.upload_latest_tweets("CALFIRES", 10)

        print("listening: ")
        self.stream.filter(follow=user_twitter_id, track=keywords)  # 876731042 is kelly
        self.text_file.close()

    def set_file(self, file):
        self.text_file = file

    def on_data(self, data):
        # write to text file
        print(data)
        print(data)
        self.text_file.write(data)
        self.text_file.flush()
        self.numTweets += 1
        time.sleep(0.1)
        data = json.loads(data)
        self.upload_data(data)
        return True

    def on_error(self, status):
        self.text_file.write(status)
        print(status)

    def upload_data(self, data):
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
        data = {"text": tweet_text, "name": tweet_name, "screen_name": tweet_screen_name, "coordinates": tweet_coords,
                "created_at": tweet_created_at}
        db.child("Tweets").child(tweet_screen_name).child(tweet_created_at).push(data)
        print("Tweet added")

        # self.screen.add_tweet(tweet_name,tweet_text,tweet_created_at)
        time.sleep(.2)

    def word_in_text(self, word, text):
        text = str(text)
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)

        if match:
            print("match")
            return True
        return False

    def upload_latest_tweets(self, name, number):
        status = self.api.user_timeline(screen_name=name, count=number)
        for tweet in status:
            self.upload_data(tweet)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    time.sleep(1.0)
    listen = StdOutListener(['876731042'], ['#NGDemo', '#NorCalFires', '#SantaRosaFire', '#HurricaneOphelia'])

    sys.exit(app.exec_())
