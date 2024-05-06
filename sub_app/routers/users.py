from fastapi import APIRouter


router = APIRouter()


@router.get('/users/', tags=["users"])
async def read_user():
    return [
        {
            "username": "some1",
        },
        {
            "username": "some2",
        },
        {
            "username": "some3",
        },
    ]
    
    
@router.get('/users/me', tags=["users"])
async def read_user_me():
    return {
        "username": "current user"
    }
    
@router.get('/users/{username}', tags=["users"])
def read_user(username: str):
    return {"username": username}