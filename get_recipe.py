import os
import requests
import random
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'spoonacular.env')
load_dotenv(dotenv_path)
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