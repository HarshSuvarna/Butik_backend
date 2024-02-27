import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.db.database import get_db
from src.schemas import User_basic, VerifyOtp
from src.services.otp_method import send_otp, verify_otp

router = APIRouter()


@router.post("/send_otp", tags=["OTP"])
def send(user: User_basic, db: Session = Depends(get_db)):
    id = uuid.uuid4()
    output = send_otp(str(id), user, db)
    return output


@router.post("/verify_otp", tags=["OTP"])
def login(verifyotp: VerifyOtp, db: Session = Depends(get_db)):
    output = verify_otp(verifyotp, db)
    return output
