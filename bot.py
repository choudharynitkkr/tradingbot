import datetime
import os
import pyotp
import requests
from smartapi import SmartConnect

def send_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def place_order(obj, variety, tradingsymbol, symboltoken, transactiontype,
                exchange, producttype, duration, price, quantity, price_type):
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "transactiontype": transactiontype,
            "exchange": exchange,
            "producttype": producttype,
            "duration": duration,
            "price": price,
            "quantity": quantity,
            "pricetype": price_type
        }
        response = obj.placeOrder(orderparams)
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}

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

        # Get LTP of RELIANCE
        ltp_data = obj.ltpData('NSE', 'RELIANCE-EQ', 'RELIANCE')
        ltp = ltp_data['data']['ltp']
        print(f"📈 RELIANCE LTP: ₹{ltp}")

        # Buy if LTP < 2500
        if ltp < 2500:
            # Find RELIANCE token to place order
            instruments = obj.getMaster("NSE")['data']
            reliance_token = None
            for instrument in instruments:
                if instrument['symbol'] == 'RELIANCE' and instrument['exchange'] == 'NSE':
                    reliance_token = instrument['token']
                    break

            if reliance_token is None:
                msg = "❌ Could not find RELIANCE token for placing order"
                print(msg)
                send_telegram(msg, telegram_token, telegram_chat_id)
                return

            print("🔄 Placing BUY order for RELIANCE...")
            order_response = place_order(
                obj=obj,
                variety="NORMAL",
                tradingsymbol="RELIANCE",
                symboltoken=reliance_token,
                transactiontype="BUY",
                exchange="NSE",
                producttype="INTRADAY",
                duration="DAY",
                price=0,             # Market order
                quantity=1,
                price_type="MARKET"
            )

            print(f"📝 Order Response: {order_response}")
            send_telegram(f"✅ BUY order placed: {order_response}", telegram_token, telegram_chat_id)
        else:
            msg = f"ℹ️ No BUY signal. RELIANCE price at ₹{ltp}"
            print(msg)
            send_telegram(msg, telegram_token, telegram_chat_id)

    except Exception as e:
        print("❌ Error:", str(e))
        send_telegram(f"❌ Bot error: {str(e)}", telegram_token, telegram_chat_id)

if __name__ == "__main__":
    run_bot()
