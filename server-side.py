import flask
import os
import get_food
import get_tweet
import get_recipe

app = flask.Flask(__name__)

@app.route("/")
def index():
    food_name = get_food.get_food()
    tweet_info = get_tweet.get_tweet(food_name)
    recipe_info = get_recipe.get_recipe_info(food_name)
   
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