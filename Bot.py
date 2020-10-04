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


# CHAT_ID = Config.data['TELEGRAM']['SUBSCRIBERS'][0]['ID']


def AddNewUser(id, status='USER'):
    TELEGRAM_USERS.append({
        'ID': id,
        'STATUS': status
    })
    Config.Save()


# Бот ждёт входящее сообщение /Start
# Бот берёт ID написавшего человека, проверяет есть ли он в списке и если нет - добавляет.


def start(update, context):
    id = update.effective_chat.id
    context.bot.send_message(chat_id=id, text="I'm a bot, please talk to me!")

    if any(x['ID'] != id for x in TELEGRAM_USERS):
        AddNewUser(id)


def add(update, context):
    text = update.message.text.replace('/add ', '').strip()

    Config.data['MESSAGES'].append(text)
    Config.Save()

    id = update.effective_chat.id
    context.bot.send_message(chat_id=id, text=f"Message '{text}' added!")


def main():
    # current_timestamp = int(time.time())  # начальное значение timestamp

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add))
    updater.start_polling()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    while True:
        messages = Config.data['MESSAGES']
        for s in TELEGRAM_USERS:
            id = s["ID"]
            message = messages[random.randint(0, len(messages) - 1)]
            print(f'Sending message "{message}" to {id}')
            bot.send_message(chat_id=id, text=message)
        time.sleep(Config.data['GLOBAL']['MESSAGE_DELAY'])


if __name__ == '__main__':
    main()
