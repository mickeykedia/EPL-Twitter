"""
Example file using Python twitter library to read 1000 tweets from Twitter and print them on
the command line.
From the tutorial: http://socialmedia-class.org/twittertutorial.html
"""
import ConfigParser
import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import timing

if __name__ == "__main__":

    # Reading Auth Credentials
    config = ConfigParser.ConfigParser()
    config.read("twitter_credentials.txt")

    ACCESS_TOKEN = config.get("auth", "access_token")
    ACCESS_SECRET = config.get("auth", "access_token_secret")
    CONSUMER_KEY = config.get("auth", "consumer_key")
    CONSUMER_SECRET = config.get("auth", "consumer_secret_key")


    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)


    iterator = twitter_stream.statuses.sample()


    tweet_count = 1000

    for tweet in iterator:
        tweet_count -= 1

        print json.dumps(tweet)

        if tweet_count <= 0:
            break




