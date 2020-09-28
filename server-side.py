import flask
import os
import tweepy
import sys
import random
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import json

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

#if (len(sys.argv) > 1):\
    #search_list = sys.argv[1:]
#else:
    #print("Please provide a list of foods at the command line.")
    #sys.exit(0)
    
search_list = ["hamburger", "spaghetti", "potatoes", "bread"]
    
#search_list = ["sushi", "onigiri", "pho", "udon", "kimchi", "tonkatsu", "bulgogi", 
               #"wonton", "yakitori", "mochi", "jiaozi", "sashimi", "ramen", "yakiniku", "wagashi"]

def get_food():
    search_item = random.choice(search_list)
    return search_item
    
food_name = get_food()
    
spoonacular_key = os.getenv('SPOONACULAR_KEY')
id_url = "https://api.spoonacular.com/recipes/complexSearch?query=" + food_name + "&number=10&apiKey=" + spoonacular_key

id_response = requests.request("GET", id_url)
id_json_body = id_response.json()
#print(id_json_body)
id_dictionary = id_json_body["results"][random.randint(0,9)]
#print(id_dictionary)
recipe_id = id_dictionary["id"]

recipe_url =  "https://api.spoonacular.com/recipes/" + str(recipe_id) + "/information?includeNutrition=false&apiKey=" + spoonacular_key
recipe_response = requests.request("GET", recipe_url)
recipe_json_body = recipe_response.json()

recipe_name = recipe_json_body["title"]
recipe_link = recipe_json_body["sourceUrl"]
recipe_time = recipe_json_body["readyInMinutes"]
recipe_image = recipe_json_body["image"]

print("ID: " + str(recipe_id))
print("Name: " + recipe_name)
print("Original Source: " + recipe_link)
print("Ready in (Minutes): " + str(recipe_time))
print("Image URL: " + recipe_image)

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