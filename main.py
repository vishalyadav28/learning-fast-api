from fastapi import FastAPI

app = FastAPI()





# @app.get('/cart_items',description='This route is for cart items')
# def cart_items():
#     return {'message':'Items list'}


# @app.get('/cart_items/{item_id}',description='This route is for cart items with specific id')
# def get_item(item_id: int):
#     return {'message':'Item details'}


## Here when you setup route like this it actually don't do the things you want

## For example :
## users/me 
## route will not return its response

## PTR(Point to remember) : That if you want to set some fix route then
## you should define before Dynamic route else you will end up in that cycle through 
## problem with fastapi


@app.put('/')
def put():
    return {'message':'Let\'s go but this first put'}


@app.get('/users')
def list_users():
    return {"message": "user list"}

# @app.get('/users/{user_id}')
# def user_data(user_id: str):
#     return {"user_id":user_id}


# @app.get('/users/me')
# def user_data():
#     return {"message":"This is the current user"}

#so actually you need to swap the functions
#define users/me first then dynamic one



@app.get('/users/me')
def user_data():
    return {"message":"This is the current user"}

# intro to path params

@app.get('/users/{user_id}')
def user_data(user_id: str):
    return {"user_id":user_id}


## Now this will work fine


## introduction to enum 
from enum import Enum

class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name" : food_name, "message":"You are healthy"}
    if food_name == FoodEnum.fruits:
        return {"food_name" : food_name, "message":"You are healthy by eating them"}

    return {"food_name" : food_name, "message":"You are healthy by dairy products"}

# intro to query params


fake_list_items = [
    {"key1":"value1"},
    {"key2":"value2"},
    {"key3":"value3"},
    {"key4":"value4"},
    {"key5":"value5"},
    {"key6":"value6"},
    {"key7":"value7"},
    {"key8":"value8"},
    {"key9":"value9"},
    {"key10":"value10"},
    ]

@app.get("/items")
def list_items(skip:int=0, limit:int=10):
    return fake_list_items[skip:skip+limit]



from typing import Optional

@app.get("/items/{item_id}")
def get_item(item_id:str, q:str | None = None):
    if q:
        return{"item_id":item_id, "q":q}
    return {"item_id":item_id}


# intro to body params

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post('/items')
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        total_price_with_tax = item.tax + item.price
        item_dict.update({"total_price_with_tax":total_price_with_tax})
    return item_dict