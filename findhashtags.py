import json
import pandas as pd
import matplotlib.pyplot as plt
import re

# test

def word_in_text(word, text):
    text = str(text)
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)

    if match:
        return True
    return False


tweets_data_path = 'Output.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
print (len(tweets_data))
tweets = pd.DataFrame()

for line in tweets_data:
    try:
        # Read in one line of the file, convert it into a json object
        #tweet = json.loads(line.strip())
        tweet = line
        if 'text' in tweet:  # only messages contains 'text' field is a tweet
            print(tweet['id'])  # This is the tweet's id
            print(tweet['created_at'])  # when the tweet posted
            print(tweet['text'])  # content of the tweet

            print(tweet['user']['id'])  # id of the user who posted the tweet
            print(tweet['user']['name'])  # name of the user, e.g. "Wei Xu"
            print(tweet['user']['screen_name'])  # name of the user account, e.g. "cocoweixu"

            hashtags = []
            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['text'])
            print(hashtags)

    except:
        continue