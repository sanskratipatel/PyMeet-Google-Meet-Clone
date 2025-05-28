from pydantic import BaseModel, EmailStr 

class RegisterRequest(BaseModel):
    username :str 
    email : EmailStr
    password:str 

class VerifyOtpRequests(BaseModel):
    email: EmailStr 
    otp: str  

