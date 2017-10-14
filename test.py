import json
import pandas as pd
import matplotlib.pyplot as plt
import re

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


tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
#plt.show()

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
#plt.show()


pythonCount = 0
javascriptCount = 0
rubyCount = 0

for tweet in tweets_data:
    if word_in_text('python', tweet):
        pythonCount+=1
    if word_in_text('javascript', tweet):
        javascriptCount+=1
    if word_in_text('ruby', tweet):
        rubyCount+=1


print (pythonCount)
print (javascriptCount)
print (rubyCount)

prg_langs = ['python', 'javascript', 'ruby']
tweets_by_prg_lang = [pythonCount,javascriptCount,rubyCount]

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. ruby (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
plt.show()