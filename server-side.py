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
    
#spoonacular_key = os.getenv('SPOONACULAR_KEY')

#def get_recipe_info(food_name):
    #id_url = "https://api.spoonacular.com/recipes/complexSearch?query=" + food_name + "&number=10&apiKey=" + spoonacular_key
    #id_response = requests.request("GET", id_url)
    #id_json_body = id_response.json()
    #id_dictionary = id_json_body["results"][random.randint(0,9)]
    #recipe_id = id_dictionary["id"]
    
    #recipe_url =  "https://api.spoonacular.com/recipes/" + str(recipe_id) + "/information?includeNutrition=false&apiKey=" + spoonacular_key
    #recipe_response = requests.request("GET", recipe_url)
    #recipe_dictionary = recipe_response.json()

    #recipe_name = recipe_dictionary["title"]
    #recipe_link = recipe_dictionary["sourceUrl"]
    #recipe_time = recipe_dictionary["readyInMinutes"]
    #recipe_image = recipe_dictionary["image"]
    
    #print("ID: " + str(recipe_id))
    #print("Name: " + recipe_name)
    #print("Original Source: " + recipe_link)
    #print("Ready in (Minutes): " + str(recipe_time))
    #print("Image URL: " + recipe_image)
    
    #recipe_info_list = []
    #recipe_info_list.append(recipe_name)
    #recipe_info_list.append(recipe_link)
    #recipe_info_list.append(recipe_time)
    #recipe_info_list.append(recipe_image)
    #return recipe_info_list

def get_tweet(food_name):
    tweets_list = []
    count = 20
    lang = "en"
    
    tweets = auth_api.search(food_name, lang, count, tweet_mode='extended')
    for tweet in tweets:
        if hasattr(tweet, 'retweeted_status'):
            contents = tweet.retweeted_status.full_text
        else:
            contents = tweet.full_text
        user = "@" + tweet.user.screen_name
        date = tweet.created_at
        url = tweet.source_url
        tweets_list.append((user, contents, date, url))
        
    chosen_tweet = random.choice(tweets_list)
    return chosen_tweet

app = flask.Flask(__name__)

@app.route("/")
def index():
    food_name = get_food()
    tweet_info = get_tweet(food_name)
    #recipe_info = get_recipe_info(food_name)
    recipe_info = ["Grilled Cheese Sandwich", "https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/", "15", "https://hips.hearstapps.com/hmg-prod/images/grilled-cheese-horizontal-jpg-1522266016.jpg"]
    return flask.render_template(
        "food_tweets.html",
        keyword = food_name,
        len_tweet = len(tweet_info),
        tweet_html = tweet_info,
        len_recipe = len(recipe_info),
        recipe_html = recipe_info
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)