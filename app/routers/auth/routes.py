from datetime import timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from routers.auth.request import RegisterRequest, VerifyOtpRequests,ForgotPasswordRequest,ResetPasswordRequest
from routers.auth.response import MessageResponse 
from models.usermodels import User, Role  
from db.database import get_db 
from auth.utils import verify_otp ,send_otp_to_user
from passlib.context import CryptContext 
from app.utils.jwt import create_access_token, create_refresh_token
from app.utils.cache import  send_otp_to_user, verify_otp
api = APIRouter(prefix="/auth" , tags = ["Auth"]) 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


@api.post("/register", response_model = MessageResponse)
def register_user(
        data: RegisterRequest, 
        db: Session = Depends(get_db)
        ): 
    existing_user = db.query(User).filter(User.email == data.email).first() 
    if existing_user:
        raise HTTPException(status_code =400,detail = "User Already Exists") 
    try : 
        hashed_password = pwd_context.hash(data.password) 
        send_otp_to_user(data.email)  
        user_email = data.email.lower()
        new_user = User( 
        username = data.username,
        email = user_email,
        password= hashed_password, 
        is_verified = False,
        role_id = None
        )
        db.add(new_user) 
        db.commit() 
        db.refresh(new_user) 
        return {"message" : "OTP send to your email."} 

    except Exception as e : 
        db.rollback() 
        raise HTTPException(status_code=500, detail = f"Error During Registration : {str(e)}")  
    

@api.post("/verify-otp", response_model = MessageResponse) 
def verify_user_otp( 
    data : VerifyOtpRequests, 
    db: Session = Depends(get_db)): 
    try:  
        user_email = data.email.lower()
        user = db.query(User).filter(User.email == user_email).first() 
        if not user: 
            raise HTTPException(status_code= 400,detail= "User not found")  
        if User.is_verified : 
            return {"message" : "User Already Verified"}
        if not verify_otp(data.email, data.otp): 
            raise HTTPException(status_code=400, detail = "Invalid OTP")
        user.is_verified = True 
        user.role_id = user 
        db.commit() 
        return {"message" : "User Sucessfully Verified "}
    except Exception as e:
       db.rollback()
       raise HTTPException(status_code = 500 ,details = f"Internal Server Error : {str(e)}")

from routers.auth.request import LoginRequest
from app.utils.jwt import create_access_token, create_refresh_token

@api.post("/login", response_model=MessageResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
    )
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    } 


@api.post("/reset-password", response_model=MessageResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP") 
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = pwd_context.hash(data.new_password)
    db.commit()
    return {"message": "Password reset successfully"}


@api.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    send_otp_to_user(data.email)
    return {"message": "OTP sent to your email"} 

