import random
from .cache import save_otp, get_otp as retrieve_otp, invalidate_otp
from app.utils.otp import save_otp, get_otp as retrieve_otp
from .email import send_email

def send_otp_to_user(email: str):
    otp = f"{random.randint(100000, 999999)}"
    save_otp(email, otp)

    subject = "Your OTP Verification Code"
    body = f"""
        <html>
            <body>
                <h2>OTP Verification</h2>
                <p>Your One-Time Password (OTP) is:</p>
                <h3>{otp}</h3>
                <p>This OTP is valid for 10 minutes. If you request a new one, the previous becomes invalid.</p>
                <br/>
                <p>Thanks,<br/>{os.getenv("EMAIL_FROM_NAME")}</p>
            </body>
        </html>
    """

    send_email(email, subject, body)

def verify_otp(email: str, otp: str) -> bool:
    saved = retrieve_otp(email)
    if saved == otp:
        invalidate_otp(email)  # OTP is one-time use
        return True
    return False
