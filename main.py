import pyotp
import dotenv
import os
import json
import cloudscraper

# load environment variables
dotenv.load_dotenv()
TOTP_SECRET = os.getenv("TOTP_SECRET")
WS_LOGIN_EMAIL = os.getenv("WEALTHSIMPLE_LOGIN_EMAIL")
WS_LOGIN_PASSWORD = os.getenv("WEALTHSIMPLE_LOGIN_PASSWORD")

# local constants
WS_BASE_URL = "https://trade-service.wealthsimple.com/"

# we use `cloudscraper` to get past Cloudflare's anti-bot page
scraper = cloudscraper.create_scraper()

def get_two_factor_otp():
    totp = pyotp.TOTP(TOTP_SECRET)
    return totp.now()


# authenticate
params = [
    ("email", WS_LOGIN_EMAIL),
    ("password", WS_LOGIN_PASSWORD),
    ("otp", get_two_factor_otp()),
]
response = scraper.post(f"{WS_BASE_URL}/auth/login", params)
scraper.headers.update({"Authorization": response.headers["X-Access-Token"]})

# get accounts list
accounts = scraper.get(f"{WS_BASE_URL}/account/list").json()["results"]
with open("accounts.json", 'w') as f:
	json.dump(accounts, f)
