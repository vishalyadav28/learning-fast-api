from datetime import timedelta,datetime
import time

from fastapi import FastAPI, Body, Cookie, Header, Form, File, Request, UploadFile, HTTPException, Depends,status, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl,EmailStr
from typing import Literal
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

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

# item = [
#     {'item1': "description"}
# ]

# @app.get('/items/{item_id}')
# def read_items(item_id: int):
#     if item_id not in item:
#         raise HTTPException(status_code=404, detail="Item not Found")
#     return {
#         "item":item[item_id],
#     }


#JSON compatibility
# from datetime import datetime

# fake_db = {}

# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: str | None = None

# @app.put('/items/{id}')
# def update_item(id: str, item:Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data
#     print(fake_db)
#     return "Success"
    
    
# (exclude_unset=True/False)  => this means it the values are provide will update it
                    # else it will ignore it
                    
                    


#Depends intro

# def common_params(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {'q': q, 'skip': skip, 'limit': limit}

# @app.get('/items')
# def read_items(common: dict = Depends(common_params)):
#     return common


# @app.get('/users')
# def read_users(common: dict = Depends(common_params)):
#     return common



#classes and Dependencies


# fake_db_items = [
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


# class CommonQueryParams:
#     def __init__(self,q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit


# @app.get('/items')
# # def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):    #can do like this also like given below
# def read_items(commons: CommonQueryParams = Depends()):
#     response = {}
#     if commons.q:
#         response.update({'q': commons.q})
#     items = fake_db_items[commons.skip : commons.skip + commons.limit]
#     response.update({'items': items})
#     return response



#Sub-Dependencies

# def query_extractor(q: str | None = None):
#     return q

# def query_or_body_extractor(q: str = Depends(query_extractor), last_query: str | None = Body(None)):
#     if q:
#         return q
#     return last_query


# @app.post('/items')
# def try_query(q_or_body: str = Depends(query_or_body_extractor)):
#     return {'q_or_body':q_or_body}


# # Dependencies in path operation
# def verify_token(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# def verify_key(x_key: str = Header(...)):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key


# # app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# #place dependencies in path if you don't want to get response value in return from them @app.get(dependencies=[])else
# #place them inside path operation definition... def read_item(x:str = Depends())
# @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
# def read_items():
#     return [{"item": "Foo"}, {"item": "Bar"}]




#day-4 Security

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fake_users_db = {
#     "johndoe": dict(
#         username="johndoe",
#         full_name="John Doe",
#         email="johndoe@example.com",
#         hashed_password="fakehashedsecret",
#         disabled=False,
#     ),
#     "alice": dict(
#         username="alice",
#         full_name="Alice Wonderson",
#         email="alice@example.com",
#         hashed_password="fakehashedsecret2",
#         disabled=True,
#     ),
# }


# def fake_hash_password(password: str):
#     return f"fakehashed{password}"


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token):
#     return get_user(fake_users_db, token)


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)

#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}




#Security with JWT

# SECRET_KEY = 'The Python guy'
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30



# fake_db = {
#     "johndoe": dict(
#         username="johndoe",
#         full_name="John Doe",
#         email="johndoe@example.com",
#         hashed_password="$2b$12$I51F/mqpZuTzgqDS5L9IzebqPVWbWlIvPoQRhnKJvoBz/ckxtPeGS",
#         disabled=False,
#     ),
#     "alice": dict(
#         username="alice",
#         full_name="Alice Wonderson",
#         email="alice@example.com",
#         hashed_password="fakehashedsecret2",
#         disabled=True,
#     ),
# }



# class Token(BaseModel):
#     access_token: str
#     token_type: str
    
    
# class TokenData(BaseModel):
#     username: str | None = None
    
# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool = False
    
# class UserInDB(User):
#     hashed_password: str
    
    
    

# pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         return UserInDB(**db[username])

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception=HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         username: str = payload.get('sub')
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError as e:
#         raise credentials_exception
    
#     user = get_user(fake_db,username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp":expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# @app.post('/token', response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_db, form_data.username,form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data = {
#             "sub":user.username,
#         },
#         expires_delta=access_token_expires
#     )
    
#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }

# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user



# Middleware

# class MyMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request:Request,call_next):
#         start_time = time.time()
#         response = await call_next(request)
#         process_time = time.time() - start_time
#         response.headers['X-Process_Time'] = str(process_time)
#         return response
        
        
        
# app.add_middleware(MyMiddleware)

# origins = ['http://127.0.0.1:8000','http://127.0.0.1:3000']
# app.add_middleware(MyMiddleware)
# app.add_middleware(CORSMiddleware,allow_origins = origins )

# @app.get('/blah')
# async def blah():
#     return {"hello world"}



# Background tasks

def write_notification(email: str, message: str):
    with open('log.txt',mode='w') as email_file:
        content = f'notification for {email}:{message}'
        email_file.write(content)
        
        
@app.post('/send_notification/{email}')
async def send_notification(email: str,backgorund_tasks: BackgroundTasks):
    backgorund_tasks.add_task(write_notification, email,message='some notification')
    return {
        'message': 'Notification sent in the background'
    }
        
