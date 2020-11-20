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

def get_food():
    search_list = ["hamburger", "spaghetti", "bread", "chicken", "pasta", "pudding", "cake", "salad", 
                   "steak", "taco", "udon", "sushi", "ramen", "pho", "bulgogi"]

    search_item = random.choice(search_list)
    return search_item
    
spoonacular_key = os.getenv('SPOONACULAR_KEY')

def get_recipe_info(food_name):
    id_url = "https://api.spoonacular.com/recipes/complexSearch?query=" + food_name + "&number=10&apiKey=" + spoonacular_key
    id_response = requests.request("GET", id_url)
    id_json_body = id_response.json()
    id_dictionary = random.choice(id_json_body["results"])
    recipe_id = id_dictionary["id"]
    
    recipe_url =  "https://api.spoonacular.com/recipes/" + str(recipe_id) + "/information?includeNutrition=false&apiKey=" + spoonacular_key
    recipe_response = requests.request("GET", recipe_url)
    recipe_dictionary = recipe_response.json()

    recipe_name = recipe_dictionary["title"]
    recipe_link = recipe_dictionary["sourceUrl"]
    recipe_time = recipe_dictionary["readyInMinutes"]
    recipe_image = recipe_dictionary["image"]
    recipe_source = recipe_dictionary["sourceName"]
    recipe_likes = recipe_dictionary["aggregateLikes"]
    recipe_score = recipe_dictionary["spoonacularScore"]
    recipe_servings = recipe_dictionary["servings"]
    ingredients_list = recipe_dictionary["extendedIngredients"]
    recipe_ingredients = []
    for ingredient in ingredients_list:
        recipe_ingredients.append(ingredient["name"])
    
    recipe_info_list = []
    recipe_info_list.append(recipe_name)
    recipe_info_list.append(recipe_link)
    recipe_info_list.append(recipe_time)
    recipe_info_list.append(recipe_image)
    recipe_info_list.append(recipe_source)
    recipe_info_list.append(str(recipe_likes))
    recipe_info_list.append(str(recipe_score))
    recipe_info_list.append(str(recipe_servings))
    recipe_info_list.append(recipe_ingredients)
    return recipe_info_list

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
    recipe_info = get_recipe_info(food_name)
   
    return flask.render_template(
        "food_tweets.html",
        keyword = food_name,
        len_tweet = len(tweet_info),
        tweet_html = tweet_info,
        len_recipe = len(recipe_info),
        recipe_html = recipe_info,
        len_ingredients = len(recipe_info[8]),
        ingredients_html = recipe_info[8]
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)