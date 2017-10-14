from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
import numpy

#Variables that contains the user credentials to access Twitter API
access_token = "919017548452003840-OoV9muwD1Ct4Vb7xpbv80WhGQKDzWUJ"
access_token_secret = "fmehS5sHuV9neS6E3CwfznHMI27NNbxbQSfYGibwiQW2t"
consumer_key = "Mv2QN24elvdC5YbqVlSeq9Iui"
consumer_secret = "tGZjOHxg9e2IHpxFENecxexXArJJI3UNmuLr7VATbFaCWdRfmf"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    numTweets = 0
    currentText = None
    currentLocation = None

    text_file = None
    def __init__(self, text_file):
        self.text_file = text_file
    def on_data(self, data):
        #write to text file
        print(data)
        text_file.write(data)
        text_file.flush()
        self.numTweets += 1
        time.sleep(0.1)


        #upload to database
        tweet = json.loads(data)
        tweetText = tweet['text']
        tweetName = tweet['name']
        tweetScreenName = tweet['screen_name']
        tweetCreatedAt = tweet['created_at']
        print(tweetText)
        return True

    def on_error(self, status):
        text_file.write(status)
        print (status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API

    text_file = open("CalFireFeed.txt", "w")
    time.sleep(1.0)
    l = StdOutListener(text_file)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    print("listening")
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(follow=['876731042'])
    text_file.close()