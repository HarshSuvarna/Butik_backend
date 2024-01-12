from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

auth_token = os.getenv("OTP_AUTH")
account_sid = os.getenv("ACCOUNT_SID")

client = Client(account_sid, auth_token)
