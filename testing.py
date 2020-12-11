import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API = str(os.environ.get("API"))

dt = datetime.now()
today = dt.strftime("%A, %B %d")
day = dt.strftime("%A")
tyme = dt.strftime("%I:%M %p")

timestamp = 1607556781
last_called = datetime.fromtimestamp(timestamp).strftime("%I:%M %p on %A, %B %d")
