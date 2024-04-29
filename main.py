from fastapi import FastAPI, Body, Cookie, Header, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, Field, HttpUrl,EmailStr
from typing import Literal


app = FastAPI()





# # @app.get('/cart_items',description='This route is for cart items')
# # def cart_items():
# #     return {'message':'Items list'}


# # @app.get('/cart_items/{item_id}',description='This route is for cart items with specific id')
# # def get_item(item_id: int):
# #     return {'message':'Item details'}


# ## Here when you setup route like this it actually don't do the things you want

# ## For example :
# ## users/me 
# ## route will not return its response

# ## PTR(Point to remember) : That if you want to set some fix route then
# ## you should define before Dynamic route else you will end up in that cycle through 
# ## problem with fastapi


# @app.put('/')
# def put():
#     return {'message':'Let\'s go but this first put'}


# @app.get('/users')
# def list_users():
#     return {"message": "user list"}

# # @app.get('/users/{user_id}')
# # def user_data(user_id: str):
# #     return {"user_id":user_id}


# # @app.get('/users/me')
# # def user_data():
# #     return {"message":"This is the current user"}

# #so actually you need to swap the functions
# #define users/me first then dynamic one



# @app.get('/users/me')
# def user_data():
#     return {"message":"This is the current user"}

# # intro to path params

# @app.get('/users/{user_id}')
# def user_data(user_id: str):
#     return {"user_id":user_id}


# ## Now this will work fine


# ## introduction to enum 
# from enum import Enum

# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"

# @app.get("/foods/{food_name}")
# def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food_name" : food_name, "message":"You are healthy"}
#     if food_name == FoodEnum.fruits:
#         return {"food_name" : food_name, "message":"You are healthy by eating them"}

#     return {"food_name" : food_name, "message":"You are healthy by dairy products"}

# # intro to query params


# fake_list_items = [
#     {"key1":"value1"},
#     {"key2":"value2"},
#     {"key3":"value3"},
#     {"key4":"value4"},
#     {"key5":"value5"},
#     {"key6":"value6"},
#     {"key7":"value7"},
#     {"key8":"value8"},
#     {"key9":"value9"},
#     {"key10":"value10"},
#     ]

# @app.get("/items")
# def list_items(skip:int=0, limit:int=10):
#     return fake_list_items[skip:skip+limit]



# from typing import Optional

# @app.get("/items/{item_id}")
# def get_item(item_id:str, q:str | None = None):
#     if q:
#         return{"item_id":item_id, "q":q}
#     return {"item_id":item_id}


# # intro to body params

# from pydantic import BaseModel

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.post('/items')
# def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         total_price_with_tax = item.tax + item.price
#         item_dict.update({"total_price_with_tax":total_price_with_tax})
#     return item_dict


## day-2
## use of Field from pydantic

# class Item(BaseModel):
#     name: str
#     description: str | None = Field(None, title="Description", max_length=300)
#     price: float = Field(..., gt=0, title="Price")
#     tax: float | None = Field(None, title="tax")



# # Here we are passing Path and Body parameters
# @app.post('/items/{item_id}')
# def update_item(item_id: int, item: Item = Body(...,embed=False)):
    # result = {"item_id":item_id, "item":item}
    # return result


## Nested models

# class Image(BaseModel):
#     url: HttpUrl
#     name: str

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: list[str] = []
#     # tags: set[str] = set()
#     # image: Image | None = None
#     image: list[Image] | None = None

# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]

# @app.post('/items/{item_id}')
# def update_item(item_id: int, item: Item):
#     result = {"item_id":item_id, "item":item}
#     return result

# @app.post('/offers')
# def create_offer(offer: Offer = Body(...,embed=True)):
#     return offer

# @app.post('/images/multiple')
# def cretae_multiple_images(images: list[Image]):
#     return images

# @app.post('/blah')
# def cretae_blah(blahs: dict[int, float]):
#     return blahs


# class Item(BaseModel):
    # name: str = Field(...,example='name')
    # description: str | None = Field(None,example='A very nice description')
    # price: float = Field(...,example=16.23)
    # tax: float | None = Field(None,example=1.2)
   

## we also like this

# @app.post('/items/{item_id}')
# def update_item(item_id: int, item: Item = Body(...,example={'name':'title','description':'description','price':'price','tax':'tax'})):
#     result = {"item_id":item_id, "item":item}
#     return result



# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
    
# @app.post('/items/{item_id}')
# def update_item(
#     item_id: int,
#     item: Item = Body(
#         ...,
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A __normal__ item works _correctly_",
#                 "value": {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 16.25,
#                     "tax": 1.67,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                 "value": {"name": "Bar", "price": "16.25"},
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "description": "Hello youtubers",
#                 "value": {"name": "Baz", "price": "sixteen point two five"},
#             },
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results



## Extra Data

# from uuid import UUID
# from datetime import datetime, timedelta, time


# @app.post('/items/{item_id}')
# def update_item(
#     item_id: UUID, 
#     start_date: datetime = Body(None),
#     end_date: datetime = Body(None),
#     repeat_at: time | None = Body(None),
#     process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date + process_after 
    
#     durations = end_date - start_date 
    
#     return {
#         'item_id': item_id,
#         'start_date': start_date,
#         'end_date': end_date,
#         'repeat_at': repeat_at,
#         'process_after': process_after,
#         'start_process': start_process,
#         'durations': durations
#     }


## Cookie and header parameter 
# @app.get('/items')
# def read_items(
#     cookie_id:str | None = Cookie,
#     accept_encoding:str | None = Header(None),
#     user_agent:str | None = Header(None),
    
#     ):
#     return {
#         'cookie_id' : cookie_id,
#         'accept_encoding': accept_encoding,
#         'user_agent': user_agent  
#     }


## we are going to handle response model

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: list[str] = []
    
    
# @app.post('/items/create')
# def create_item(item: Item):
#     return item


# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserOut(UserBase):
#     pass

# class UserIn(UserBase):
#     password: str


# @app.post('/users/', response_model=UserOut)
# def create_user(user: UserIn):
#     return user


## learn about response_model, response_model_exclude_unset

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = 1.5
#     tags: list[str] = []
    
# items = {
#     "foo":{"name":"Foo", "price":54.2},
#     "bar":{"name":"Bar", "description":"something here ", "price":54.2, "tax":22.2},
# }


# @app.get('/items/{item_id}', response_model=Item, response_model_exclude_unset=True)
# def read_item(item_id: Literal["foo","bar"]):
#     return items[item_id]


## Extra model


# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserOut(UserBase):
#     pass

# class UserIn(UserBase):
#     password: str
    
# class UserInDB(BaseModel):
#     hashed_password: str
    


# def fake_password_hasher(raw_password:str):
#     return f"supersecret{raw_password}"
# def fake_save_user(user_in:UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("user saved...")
#     return user_in_db

# @app.post('/users/', response_model=UserOut)
# def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved


# Response status code

# @app.post('/items/', status_code=201)
# def create_item(name: str):
#     return {
#         'name': name,
#     }


# form fields

# class User(BaseModel):
#     username: str
#     password: str

# @app.post('/login/')
# def login(username: str = Form(...), password: str = Form(...)):
#     return {'username':username}

#Request file

# @app.post('/files')
# def create_file(file: bytes = File(...)):
#     return {'file': len(file)}


# @app.post('/Uploadfiles')
# def create_upload_file(file: UploadFile):
#     return {'file': file}



#Request Form and Files

# @app.post('/files')
# def create_files(
#     filea: bytes = File(...),
#     fileb: bytes = UploadFile(...),
#     token: str = Form(...),
#     hello: str = Body(...),
# ):
#     return {'filea':filea, 'fileb':fileb,'token': token,'hello':hello}


#Handling errors

item = [
    {'item1': "description"}
]

@app.get('/items/{item_id}')
def read_items(item_id: int):
    if item_id not in item:
        raise HTTPException(status_code=404, detail="Item not Found")
    return {
        "item":item[item_id],
    }
