import os
from os.path import join, dirname
import random
import tweepy
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "twitter.env")
load_dotenv(dotenv_path)

twitter_api_key = os.getenv("TWITTER_API_KEY")
twitter_api_key_secret = os.getenv("TWITTER_API_KEY_SECRET")
twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
auth_api = tweepy.API(auth)


def get_tweet(food_name):
    tweets_list = []
    count = 20
    lang = "en"

    if food_name is not "":
        tweets = auth_api.search(food_name, lang, count, tweet_mode="extended")
        if tweets:
            for tweet in tweets:
                if hasattr(tweet, "retweeted_status"):
                    contents = tweet.retweeted_status.full_text
                else:
                    contents = tweet.full_text
                user = "@" + tweet.user.screen_name
                date = tweet.created_at
                url = tweet.source_url
                tweets_list.append((user, contents, date, url))

            chosen_tweet = random.choice(tweets_list)
            return chosen_tweet
    else:
        chosen_tweet = "Sorry, no tweets available"
        return chosen_tweet
