import pandas as pd
from typing import Dict
import json
import tweepy as tw
import datetime
import os
import requests
import re



# your Twitter API key and API secret
with open("auth.json", "r") as f:
    data = json.load(f)

# Authenticate to Twitter
auth = tw.OAuthHandler(data["CONSUMER_KEY"], data["CONSUMER_SECRET"])
auth.set_access_token(data["ACCESS_TOKEN"], data["ACCESS_TOKEN_SECRET"])

# Create API object
api = tw.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")