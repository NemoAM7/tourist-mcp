import os
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

assert AUTH_TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert GOOGLE_MAPS_API_KEY is not None, "Please set GOOGLE_MAPS_API_KEY in your .env file"