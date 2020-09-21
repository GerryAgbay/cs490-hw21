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


if (len(sys.argv) > 1):\
    search_list = sys.argv[1:]
else:
    print("Please provide a list of foods at the command line.")
    sys.exit(0)
    

def get_item():
    index = random.randint(0, len(search_list)-1)
    search_item = search_list[index]
    return search_item


app = flask.Flask(__name__)

@app.route("/")
def index():
    tweet_list = []
    count = 10
    lang = "en"
    search = get_item()

    for tweets in auth_api.search(search, lang, count):
        screen_name = tweets.user.screen_name
        contents = tweets.text
        date = tweets.created_at
        tweet_list.append(f"{screen_name}   -----   {date}   -----   {contents}")
        
    rand_idx = random.randint(0, count-1)
    print(tweet_list[rand_idx])
    info = tweet_list[rand_idx]
    
    return flask.render_template(
        "food_tweets.html",
        information = info,
        keyword = search
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)