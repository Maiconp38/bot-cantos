from flask import Flask
from threading import Thread
from telegram import Bot
import os
import time

app = Flask(__name__)
bot = Bot(token=os.getenv("BOT_TOKEN"))

@app.route('/')
def home():
    return "✅ Robô de escanteios está rodando!"

def start_bot():
    chat_id = os.getenv("CHAT_ID")
    while True:
        bot.send_message(chat_id=chat_id, text="⚽ Robô ativo! (exemplo)")
        time.sleep(3600)

if __name__ == '__main__':
    Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=8080)
