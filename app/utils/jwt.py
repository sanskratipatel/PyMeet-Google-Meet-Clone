from datetime import datetime ,timedelta 
from jose import jwt 
import os 

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")  

def create_access_token(data: dict,expires_delta:timedelta): 
    to_encode =data.copy() 
    expire = datetime.utcnow() + expires_delta 
    to_encode.update({"exp" : expire}) 
    return jwt.encode(to_encode,JWT_SECRET_KEY, algorithm="HS256") 

def can_refresh_token(data:dict, expires_delta: timedelta):
    to_encode = data.copy() 
    expire = datetime.utcnow() + expires_delta 
    to_encode.update({"exp" : expire}) 
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm="HS256") 

