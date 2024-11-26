#  Author: Gustavo Lebre
# Created on 2024-11-21

import tweepy
import time

# Step 1: Authenticate to Twitter
API_KEY = 'NcpRqGlBCBokXZ9T3rYInoMyY'
API_SECRET = 'AFV5x07qlYiFp0hWEttKffMcXM7elCA29rlqAFtqvcNVDaBiEX'
ACCESS_TOKEN = '1216116091044487169-WetyKZKUJGiTHF3ujqckPEIw8QY5qG'
ACCESS_TOKEN_SECRET = 'B8mzR80s12MUOo2u31cE1gWzQ3JgPpZ3kyhTDqpMXXz6h'
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAJ%2F1oQEAAAAAVuxvIeRAuIf729V%2BXJVhO79lp0M%3Ddrf9vOuJplZq4M6PFNLbKtWMVusraIx9u8zqMuoLeJDHDtLp8X"


client = tweepy.Client(bearer_token, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Step 2: Set up Tweepy authentication
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Step 3: Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)


class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        try:
            client.create_tweet(in_reply_to_tweet_id=tweet.id, text="Hey there!")

        except Exception as e:
            print(e)


stream = MyStream(bearer_token=bearer_token)

rule = tweepy.StreamRule("@Guzaoow")

stream.add_rules(rule, dry_run=True)

stream.filter()

