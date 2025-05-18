import datetime
import os
import pyotp
import requests
from smartapi import SmartConnect

def send_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def run_bot():
    api_key = os.getenv("API_KEY")
    client_id = os.getenv("CLIENT_ID")
    pin = os.getenv("PIN")
    totp_token = os.getenv("TOTPTOKEN")
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

    try:
        obj = SmartConnect(api_key=api_key)
        totp = pyotp.TOTP(totp_token).now() if totp_token else None
        session = obj.generateSession(client_id, pin, totp)
        print("✅ Logged into SmartAPI")

        # Example: Get LTP of RELIANCE
        ltp_data = obj.ltpData('NSE', 'RELIANCE-EQ', 'RELIANCE')
        ltp = ltp_data['data']['ltp']
        print(f"📈 RELIANCE LTP: ₹{ltp}")

        # Simple strategy: Buy if LTP < ₹2500
        if ltp < 2500:
            msg = f"✅ BUY Signal: RELIANCE is at ₹{ltp}"
        else:
            msg = f"ℹ️ No trade. RELIANCE is at ₹{ltp}"

        print("📨 Sending Telegram message...")
        send_telegram(msg, telegram_token, telegram_chat_id)

    except Exception as e:
        print("❌ Error:", str(e))
        send_telegram(f"❌ Bot error: {str(e)}", telegram_token, telegram_chat_id)

if __name__ == "__main__":
    run_bot()
