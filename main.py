import requests
import wealthsimple
import pyotp
import dotenv
import os
import json

# load environment variables
dotenv.load_dotenv()
TOTP_SECRET = os.getenv("TOTP_SECRET")
WS_LOGIN_EMAIL = os.getenv("WEALTHSIMPLE_LOGIN_EMAIL")
WS_LOGIN_PASSWORD = os.getenv("WEALTHSIMPLE_LOGIN_PASSWORD")

totp = pyotp.TOTP(TOTP_SECRET)


def get_two_factor_otp():
    return totp.now()


ws = wealthsimple.WSTrade(
    WS_LOGIN_EMAIL, WS_LOGIN_PASSWORD, two_factor_callback=get_two_factor_otp
)

a = ws.get_accounts()
with open("output.json", "w") as f:
    json.dump(a, f)
