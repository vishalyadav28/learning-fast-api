from fastapi import FastAPI, Depends


from .dependencies import get_token_header, get_query_token

from .routers import users_router, items_router


# from .routers.users import router
# from .routers.items import router

# app.include_router(router)


# from .routers import users, items
# app.include_router(users.router)
# app.include_router(items.router)

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users_router)
app.include_router(items_router)

@app.get('/')
async def root():
    return {
        'message':'Hello Massive!!'
    }