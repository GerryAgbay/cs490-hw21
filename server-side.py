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
    search_item = random.choice(search_list)
    return search_item


app = flask.Flask(__name__)

@app.route("/")
def index():
    tweet_list = []
    count = 20
    lang = "en"
    search = get_item()
    
    tweets = auth_api.search(search, lang, count)
    for tweet in tweets:
        user = "@" + tweet.user.screen_name
        contents = tweet.text
        date = tweet.created_at
        url = tweet.source_url
        tweet_list.append((user, contents, date, url))
        
    info = random.choice(tweet_list)
    headers = ["User", "Tweet", "Date", "URL"]
    
    return flask.render_template(
        "food_tweets.html",
        len_info = len(info),
        info_html = info,
        len_headers = len(headers),
        headers_html = headers,
        keyword = search
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)