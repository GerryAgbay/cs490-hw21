import random


def get_food():
    search_list = [
        "hamburger",
        "spaghetti",
        "bread",
        "chicken",
        "pasta",
        "pudding",
        "cake",
        "salad",
        "steak",
        "taco",
        "udon",
        "sushi",
        "ramen",
        "pho",
        "bulgogi",
    ]

    search_item = random.choice(search_list)
    return search_item
