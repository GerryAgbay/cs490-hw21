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
    

tweet_list = []
count = 10
lang = "en"
search = get_item()

for tweet in Cursor(auth_api.search, search, lang, tweet_mode='extended').items(count):
    screen_name = tweet.user.screen_name
    contents = tweet.full_text
    date = tweet.created_at
    tweet_list.append(f"{screen_name}   -----   {date}   -----   {contents}")


rand_idx = random.randint(0, 9)
print(tweet_list[rand_idx])


app = flask.Flask(__name__)

@app.route('/')
def index():
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