import os
import requests
import telegram
import time
import Config
from telegram.ext import Updater
from telegram.ext import CommandHandler
import random

Config.Load()

TELEGRAM_TOKEN = Config.data['TELEGRAM']['TOKEN']
TELEGRAM_USERS = Config.data['TELEGRAM']['SUBSCRIBERS']
#CHAT_ID = Config.data['TELEGRAM']['SUBSCRIBERS'][0]['ID']


def AddNewUser(id, status='USER'):
    TELEGRAM_USERS.append({
        'ID': id,
        'STATUS': status
    })
    Config.Save()

# Бот ждёт входящее сообщение /Start
# Бот берёт ID написавшего человека, проверяет есть ли он в списке и если нет - добавляет.


def send_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    return bot.send_message(chat_id=CHAT_ID, text=message)


def start(update, context):
    id = update.effective_chat.id
    context.bot.send_message(chat_id=id, text="I'm a bot, please talk to me!")

    if any(x['ID'] != id for x in TELEGRAM_USERS):
        AddNewUser(id)

messages = None

def LoadMessages():
    global messages
    r = requests.get("https://raw.githubusercontent.com/atmay/MyInspirationBot/master/Messages.txt")
    lines = r.text.split("\n")
    messages = [line.strip() for line in lines]


def main():
    global messages
    LoadMessages()
    # current_timestamp = int(time.time())  # начальное значение timestamp

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    while True:
        for s in TELEGRAM_USERS:
            id = s["ID"]
            message = messages[random.randint(0, len(messages))]
            print(f'Sending message "{message}" to {id}')
            bot.send_message(chat_id=id, text=message)
        time.sleep(Config.data['GLOBAL']['MESSAGE_DELAY'])
        # try:
        #     new_homework = get_homework_statuses(current_timestamp)
        #     if new_homework.get('homeworks'):
        #         send_message(parse_homework_status(new_homework.get('homeworks')[0]))
        #     current_timestamp = new_homework.get('current_date')  # обновить timestamp
        #
        #
        # except Exception as e:
        #     print(f'Бот упал с ошибкой: {e}')
        #     time.sleep(5)
        #     continue


if __name__ == '__main__':
    main()
