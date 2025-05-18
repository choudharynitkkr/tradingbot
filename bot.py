import datetime
import os

api_key = os.getenv("API_KEY")
client_id = os.getenv("CLIENT_ID")
pin = os.getenv("PIN")
totp_token = os.getenv("TOTPTOKEN")  # Optional, can be None
telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Example usage:
print(f"Using API key: {api_key}")

def run_bot():
    now = datetime.datetime.now()
    print(f"Running bot at {now}")

if __name__ == "__main__":
    run_bot()
