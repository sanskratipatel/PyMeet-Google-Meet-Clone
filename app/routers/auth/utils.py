import random 
from utils.email import send_otp_email
import asyncio


otp_store = {} 

def generate_otp(email:str) -> str:
    otp = str(random.randint(100000, 999999)) 
    otp_store[email] = otp 
    return otp 

def verify_otp(email:str, otp:str) ->bool :
    return otp_store.get(email) == otp 


def send_otp_to_user(email: str) -> str:
    otp = generate_otp(email)
    asyncio.create_task(send_otp_email(email, otp))  # Send email asynchronously
    return otp

