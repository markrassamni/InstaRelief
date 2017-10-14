from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#Variables that contains the user credentials to access Twitter API
access_token = "919017548452003840-OoV9muwD1Ct4Vb7xpbv80WhGQKDzWUJ"
access_token_secret = "fmehS5sHuV9neS6E3CwfznHMI27NNbxbQSfYGibwiQW2t"
consumer_key = "Mv2QN24elvdC5YbqVlSeq9Iui"
consumer_secret = "tGZjOHxg9e2IHpxFENecxexXArJJI3UNmuLr7VATbFaCWdRfmf"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, text_file):
        self.text_file = text_file
    def on_data(self, data):
        text_file.write(data)
        print (data)
        return True

    def on_error(self, status):
        text_file.write(status)
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    text_file = open("Output.txt", "w")

    l = StdOutListener(text_file)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)


    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['fire', 'police', 'ruby'])

    text_file.close()