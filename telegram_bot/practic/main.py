import subprocess
import threading
import uvicorn

from web.api import app


def start_bot():
    subprocess.run(['python3', 'telegram_bot/bot.py'])
#

def start_server():
    uvicorn.run(app, port=8080)


if __name__ == '__main__':
    bot_thread = threading.Thread(target=start_bot)
    server_thread = threading.Thread(target=start_server)

    bot_thread.start()
    server_thread.start()
