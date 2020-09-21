import flask
import os
import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import sys
import random

twitter_api_key = os.environ['TWITTER_API_KEY']
twitter_api_key_secret = os.environ['TWITTER_API_KEY_SECRET']

auth = OAuthHandler(twitter_api_key, twitter_api_key_secret)
auth_api = API(auth)

text_query = "food"
tweet_list = []
count = 10

def get_tweets():
    lang = "en"

    for tweet in auth_api.search(text_query, lang, count):
        tweet_list.append(f"{tweet.user.screen_name}  -----  {tweet.text}")
        #print(tweet.user.name + " ----- " + tweet.text)

get_tweets()
rand_idx = random.randint(0, 9)
print(tweet_list[rand_idx])

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)