from fastapi import HTTPException, Header


async def get_token_header(x_token: str = Header(...,example='fake-token')):
    if x_token != 'fake-token':
        raise HTTPException(status_code=404, detail='X-Token is not a valid token')
    
    
    
    
async def get_query_token(token: str = 'fake'):
    if token != 'fake':
        raise HTTPException(status_code=400, detail='No Token Provided')
    
