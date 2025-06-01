import time
from typing import Dict, Tuple

otp_cache: Dict[str, Tuple[str, float]] = {} 

def save_otp(email: str, otp: str, ttl: int = 600):
    """
    Save or overwrite OTP for an email with a TTL in seconds.
    """
    otp_cache[email] = (otp, time.time() + ttl)

def get_otp(email: str) -> str:
    """
    Retrieve OTP if it hasn’t expired. Else return None.
    """
    data = otp_cache.get(email)
    if data:
        otp, expiry = data
        if time.time() < expiry:
            return otp
        else:
            del otp_cache[email]  # clean up expired entry
    return None

def invalidate_otp(email: str):
    """
    Manually remove the OTP (e.g. when resending or successful verification).
    """
    otp_cache.pop(email, None)
