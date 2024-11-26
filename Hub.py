# File: main.py
import schedule
import time
from datetime import datetime

import tweepy
from tweepy import Client

# Import message functions from the respective files
import bitcoin_price

# Twitter API credentials
API_KEY = 'NcpRqGlBCBokXZ9T3rYInoMyY'
API_SECRET = 'AFV5x07qlYiFp0hWEttKffMcXM7elCA29rlqAFtqvcNVDaBiEX'
ACCESS_TOKEN = '1216116091044487169-WetyKZKUJGiTHF3ujqckPEIw8QY5qG'
ACCESS_TOKEN_SECRET = 'B8mzR80s12MUOo2u31cE1gWzQ3JgPpZ3kyhTDqpMXXz6h'
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAJ%2F1oQEAAAAAVuxvIeRAuIf729V%2BXJVhO79lp0M%3Ddrf9vOuJplZq4M6PFNLbKtWMVusraIx9u8zqMuoLeJDHDtLp8X"

# Initialize Twitter client
client = tweepy.Client(bearer_token, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Step 2: Set up Tweepy authentication
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Step 3: Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet(text):
    client.create_tweet(text=text)


def post_crypto_updates():
    """Fetches messages for all cryptocurrencies and posts them on Twitter."""
    try:
        # Fetch messages
        (
            btc_message,
            btc_lowest_price,
            btc_highest_price,
            btc_now_price,
            change,
            btc_emoji,
        ) = bitcoin_price.get_bitcoin_price_message()

        # Validate data before comparing
        if btc_lowest_price is None or btc_highest_price is None or btc_now_price is None:
            print("Error: Missing data for Bitcoin prices. Skipping further checks.")
            return

        # Print message
        print(btc_message)
     
        tweet(btc_message)
        time.sleep(120)
        

        # Check if the current price is a new lowest or highest
        if btc_now_price < btc_lowest_price:
            btc_record_message = (
                f"Bitcoin price has reached its LOWEST price in the last 3 months.\n"
                f"Bitcoin price is now at ${btc_now_price:.2f}. ({change:+.2f}% {btc_emoji})"
            )
            print(btc_record_message)
            tweet(btc_record_message)
            time.sleep(120)
        elif btc_now_price > btc_highest_price:
            btc_record_message = (
                f"Bitcoin price has reached its HIGHEST price in the last 3 months.\n"
                f"Bitcoin price is now at ${btc_now_price:.2f}. ({change:+.2f}% {btc_emoji})"
            )
            tweet(btc_record_message)
            time.sleep(120)

    except Exception as e:
        print(f"Error posting updates: {e}")


# Schedule the task to run daily at 12:00 PM EST
# schedule.every().day.at("12:00").do(post_crypto_updates)

print("Scheduler is running. Waiting for tasks...")

# Run pending tasks
# schedule.run_pending()
# time.sleep(1)
post_crypto_updates()
