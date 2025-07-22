import yfinance as yf
import time
import telebot
from datetime import datetime

TOKEN = "8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs"
CHAT_ID = "5556108366"

bot = telebot.TeleBot(TOKEN)

symbols = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CHF": "CHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "CAD=X"
}

def get_signal(data):
    try:
        if data.empty or len(data) < 2:
            return None, 0

        last = data.iloc[-1]
        prev = data.iloc[-2]

        direction = ""
        confidence = 0

        if last["Close"] > last["Open"] and prev["Close"] > prev["Open"]:
            direction = "BUY"
            confidence = 80
        elif last["Close"] < last["Open"] and prev["Close"] < prev["Open"]:
            direction = "SELL"
            confidence = 80

        return direction, confidence
    except Exception as e:
        return None, 0

def send_message(message):
    bot.send_message(CHAT_ID, message)

while True:
    for name, symbol in symbols.items():
        try:
            data = yf.download(tickers=symbol, interval="1m", period="5d")
            signal, confidence = get_signal(data)

            if signal:
                price = data["Close"].iloc[-1]
                message = (
                    f"📊 *{name}*\n"
                    f"🕒 {datetime.now().strftime('%H:%M:%S')}\n"
                    f"💰 Цена: {price:.5f}\n"
                    f"📈 Сигнал: *{signal}*\n"
                    f"✅ Уверенность: {confidence}%\n"
                    f"⏱ Вход: 1-3 минуты"
                )
                bot.send_message(CHAT_ID, message, parse_mode="Markdown")
            else:
                bot.send_message(CHAT_ID, f"⚠️ {name}: нет надёжного сигнала.")
        except Exception as e:
            bot.send_message(CHAT_ID, f"❌ Ошибка {name}: {str(e)}")
    time.sleep(30)
