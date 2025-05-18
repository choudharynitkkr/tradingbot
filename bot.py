import datetime
import os

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

def run_bot():
    now = datetime.datetime.now()
    print(f"Running bot at {now}")

if __name__ == "__main__":
    run_bot()
