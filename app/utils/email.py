from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()  

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_TLS=os.getenv("MAIL_TLS") == "True",
    MAIL_SSL=os.getenv("MAIL_SSL") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_otp_email(email: EmailStr, otp: str):
    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP is: {otp}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
