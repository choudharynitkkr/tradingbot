import datetime
import os

def run_bot():
    api_key = os.getenv("API_KEY")
    client_id = os.getenv("CLIENT_ID")
    pin = os.getenv("PIN")
    totp_token = os.getenv("TOTPTOKEN")  # Optional
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Check required secrets
    required = [api_key, client_id, pin, telegram_token, telegram_chat_id]
    if not all(required):
        print("❌ Missing one or more required environment variables!")
        return

    print(f"✅ Using API_KEY: {api_key[:4]}****")
    print(f"✅ CLIENT_ID: {client_id}")
    print(f"✅ PIN: {'*' * len(pin)}")
    if totp_token:
        print("✅ TOTP Token provided")
    else:
        print("ℹ️ No TOTP Token (optional)")
    print(f"✅ Telegram Token: {telegram_token[:4]}****")
    print(f"✅ Telegram Chat ID: {telegram_chat_id}")

    now = datetime.datetime.now()
    print(f"🕒 Running bot at {now}")

if __name__ == "__main__":
    run_bot()
