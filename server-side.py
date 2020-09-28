import flask
import os
import tweepy
import sys
import random
import requests
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'twitter.env')
load_dotenv(dotenv_path)

twitter_api_key = os.getenv('TWITTER_API_KEY')
twitter_api_key_secret = os.getenv('TWITTER_API_KEY_SECRET')
twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
auth_api = tweepy.API(auth)

dotenv_path = join(dirname(__file__), 'spoonacular.env')
load_dotenv(dotenv_path)

spoonacular_key = os.getenv('SPOONACULAR_KEY')
url = 'https://api.spoonacular.com/recipes/search?apiKey={}'.format(spoonacular_key)

response = requests.get(url)
json_body = response.json()
print(json_body)

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
    
    tweets = auth_api.search(search, lang, count, tweet_mode='extended')
    for tweet in tweets:
        if hasattr(tweet, 'retweeted_status'):
            contents = tweet.retweeted_status.full_text
        else:
            contents = tweet.full_text
        user = "@" + tweet.user.screen_name
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