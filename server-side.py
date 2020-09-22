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

#if (len(sys.argv) > 1):\
    #search_list = sys.argv[1:]
#else:
    #print("Please provide a list of foods at the command line.")
    #sys.exit(0)
    
search_list = ["sushi", "onigiri", "pho", "udon", "kimchi", "tonkatsu", "bulgogi", 
               "wonton", "yakitori", "mochi", "jiaozi", "sashimi", "ramen", "yakiniku", "wagashi"]

def get_food():
    search_item = random.choice(search_list)
    return search_item

def get_tweets():
    tweets_list = []
    count = 20
    lang = "en"
    search = get_food()
    
    tweets = auth_api.search(search, lang, count)
    for tweet in tweets:
        user = "@" + tweet.user.screen_name
        contents = tweet.text
        date = tweet.created_at
        url = tweet.source_url
        tweets_list.append((user, contents, date, url))
    
    information = [search, tweets_list]
    return information

app = flask.Flask(__name__)

@app.route("/")
def index():
    info = get_tweets()
    tweet = random.choice(info[1])
    return flask.render_template(
        "food_tweets.html",
        len_tweet = len(tweet),
        tweet_html = tweet,
        keyword = info[0]
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)