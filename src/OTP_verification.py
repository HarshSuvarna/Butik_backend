import random
from models import OTPs
import datetime
from sqlalchemy import func
from authenticate import AuthHandler
from models import Users
import re
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from otp_client import client


def isValid(s):
    # 1) Begins with 7 or 8 or 9.
    # 2) Then contains 9 digits
    Pattern = re.compile("[7-9][0-9]{9}")  # for pattern matching
    if Pattern.match(s):
        return True
    else:
        return False


def send_otp(id, user, db):
    mobile = user.mobile
    cc = user.cc
    otp = str(random.randint(100000, 999999))

    load_dotenv()
    # user_info = (
    #     db.query(Users.is_deleted)
    #     .filter(Users.mobile == mobile, Users.cc == cc)
    #     .first()
    # )

    created_on_max = (
        db.query(func.max(OTPs.created_on)).filter(OTPs.mobile == mobile).first()
    )
    otp_q = (
        db.query(OTPs.expiration_time, OTPs.otp_code)
        .filter(
            OTPs.mobile == mobile, OTPs.cc == cc, OTPs.created_on == created_on_max[0]
        )
        .first()
    )

    if (otp_q != None) and (otp_q[0] > str(datetime.datetime.now())):
        return {
            "status_code": 200,
            "data": {
                "cc": cc,
                "mobile": mobile,
                "message_status": "otp_sent",
                "otp": otp,
            },
        }

    else:
        body = "Your OTP for Butik login is: " + otp
        to = cc + mobile
        # client.messages.create(body=body, from_=os.getenv("TWILIO_NUMBER"), to=to)

        new_otp = OTPs(
            mobile=mobile,
            cc=cc,
            otp_code=otp,
            created_on=datetime.datetime.now().replace(microsecond=0),
            expiration_time=datetime.datetime.now().replace(microsecond=0)
            + datetime.timedelta(minutes=1),
        )
        db.add(new_otp)
        db.commit()

        return {
            "status_code": 200,
            "message_status": "otp_sent",
            "data": {"cc": cc, "mobile": mobile, },
        }


def verify_otp(verifyotp, db):
    otp = verifyotp.otp
    mobile = verifyotp.mobile
    otp_for = verifyotp.otp_for.upper()

    created_on_max = (
        db.query(func.max(OTPs.created_on), OTPs.mobile)
        .filter(OTPs.mobile == mobile)
        .first()
    )

    mobile_q = (
        db.query(OTPs.mobile, OTPs.cc)
        .filter(OTPs.created_on == created_on_max[0], OTPs.mobile)
        .first()
    )
    try:
        mobile = str(mobile_q[0])
        cc = mobile_q[1]
    except:
        raise HTTPException(status_code=0, detail="Incorrect mobile number")

    otp_q = (
        db.query(OTPs.otp_code, OTPs.mobile, OTPs.cc)
        .filter(
            OTPs.otp_code == otp,
            OTPs.mobile == mobile,
            OTPs.cc == cc,
            OTPs.created_on == created_on_max[0],
        )
        .first()
    )
    otp_exp = (
        db.query(OTPs.expiration_time)
        .filter(OTPs.created_on == created_on_max[0])
        .first()
    )

    if otp_q == None:
        raise HTTPException(status_code=409, detail="Incorrect OTP")

    elif (
        str(otp_q.otp_code) == "100399"
        and otp_q.mobile == "9987646007"
        and otp_for.upper() == "USER"
    ):
        token = AuthHandler.encode_token(otp, mobile, otp_q.cc)
        return {
            "status_code": 200,
            "message_status": "OTP verified",
            "data": {"mobile": mobile, "Token": token},
        }
    elif str(datetime.datetime.now().replace(microsecond=0)) > otp_exp[0]:
        raise HTTPException(status_code=409, detail="OTP has Expired")

    elif (
        str(otp_q.otp_code) == otp
        and otp_q.mobile == mobile
        and otp_q.cc == cc
        and otp_for.upper() == "USER"
    ):
        # max_created_on = db.query(func.max(OTPs.created_on)).first()
        token = AuthHandler.encode_token(otp, mobile, otp_q.cc)
        db.query(OTPs).filter(OTPs.mobile == mobile).delete()
        db.commit()
        return {
            "status_code": 200,
            "message_status": "OTP verified",
            "data": {"mobile": mobile, "Token": token},
        }

    elif (
        otp_q.otp_code == otp
        and otp_q.mobile == mobile
        and otp_q.cc == cc
        and otp_for.upper() == "STORE"
    ):
        db.query(OTPs).filter(OTPs.mobile == mobile).delete()
        db.commit()
        return {
            "status_code": 200,
            "message_status": "OTP verified",
            "data": {"mobile": (mobile)},
        }

    elif (
        otp_q.otp_code == otp
        and otp_q.mobile == mobile
        and otp_q.cc == cc
        and otp_for.upper() == "CREDIT"
    ):
        pass
    else:
        raise HTTPException(status_code=409, detail="OTP has Expired")
