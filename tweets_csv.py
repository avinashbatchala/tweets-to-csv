from tweepy.streaming import StreamListener #prints live tweets to console
from tweepy import OAuthHandler #Authenticates User APIs
from tweepy import Stream
import json
import pandas as pd

# Twitter API keys are generted using twitter developer account. https://dev.twitter.com/apps/new, use this link to generate API keys
'''
Replaces the empty strings with API keys genrated, I removed them here as they are private
'''
access_token = "YOUR ACCESS TOKEN GOES HERE"
access_token_secret = "YOUR ACCESS TOKEN SECRET GOES HERE"
consumer_key = "YOUR CONSUMER KEY GOES HERE"
consumer_secret = "YOUR CONSUMER KEY SECRET GOES HERE"

# List of keywords that must be included in the tweets, which we will extract
hash_tags = ['COVID-19', '#stayhome', '#productivity']

# Initialize Global Count variable
count = 0

# Input number of tweets to be downloaded
num_tweets = 1000

# Create the class that will handle the tweet stream.
class StdOutListener(StreamListener):
    '''
    This class is taken from tweepy documentation and a minor modification is made to download reuired number of tweets.
    '''
    def on_data(self, data):
        global count
        global num_tweets
        global stream
        if count < num_tweets:
            file = open("tweets1.txt", "a")
            file.write(data)
            file.close()
            if count%1000 == 0:
              print("Tweet", count, "is Saved")
            count += 1
            return True
        else:
            stream.disconnect()

    def on_error(self, status):
        print(status)


# Handles Twitter authentication
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

stream.filter(languages=["en"], track=hash_tags)  #stream.filter param is used to extract only desired tweets. In this program the params used are languages=['en'], this is used to extract only tweets in english language.

tweets_data_path = "tweets1.txt"  
tweets_data = []  
tweets_file = open(tweets_data_path, "r")  
for line in tweets_file:  
    try:  
        tweet = json.loads(line)  
        tweets_data.append(tweet)  
    except:  
        continue
tweets = pd.DataFrame()
tweets['tweet'] = list(map(lambda tweet: tweet['text'], tweets_data))
tweets['username'] = list(map(lambda tweet: tweet['user']['screen_name'], tweets_data))
tweets['timestamp'] = list(map(lambda tweet: tweet['created_at'], tweets_data))
tweets['location'] = list(map(lambda tweet: tweet['user']['location'], tweets_data))
tweets['likes'] = list(map(lambda tweet: tweet['user']['favourites_count'], tweets_data))
df.to_csv('twitter_data.csv')
