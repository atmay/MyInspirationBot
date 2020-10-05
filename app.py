import os
import requests
import telegram
import time
import config
from telegram import Update, Message
from telegram.ext import Updater
from telegram.ext import CommandHandler
import random
import templates

config.Load()

TELEGRAM_TOKEN: str = config.data['telegram']['token']
TELEGRAM_USERS: dict = config.data['telegram']['users']


def add_new_user(id, name, status='user'):
    TELEGRAM_USERS[str(id)] = {
        'id': id,
        'name': name,
        'status': status,
        'mute': False
    }
    config.Save()


def get_user(uid):
    if isinstance(uid, Update):
        uid = uid.message.from_user.id
    uid = str(uid)
    return TELEGRAM_USERS[uid] if uid in TELEGRAM_USERS else None


def get_user_and_status(source):
    user = get_user(source)
    is_admin = user and user['status'] == 'admin'
    is_moder = user and user['status'] == 'moder'
    return user, is_admin, is_moder


def start(update: Update, context):
    user, is_admin, is_moder = get_user_and_status(update)
    id = update.message.from_user.id
    context.bot.send_message(
        chat_id=id,
        text=templates.start_message_admin if is_admin else templates.start_message)

    if id not in TELEGRAM_USERS:
        add_new_user(id, update.message.from_user.first_name)


# Main functions


def cmd_add(update: Update, context):
    user, is_admin, is_moder = get_user_and_status(update)

    text = update.message.text.replace('/add ', '').strip()

    config.data['messages'].append(text)
    config.Save()

    context.bot.send_message(
        chat_id=user['id'],
        text=templates.add_message_success.format(text=text))


def cmd_mute(update: Update, context):
    user, is_admin, is_moder = get_user_and_status(update)
    text = update.message.text.replace('/mute', '').strip()
    if text == '':
        user['mute'] = not user['mute']
    elif text == 'on':
        user['mute'] = True
    elif text == 'off':
        user['mute'] = False
    else:
        context.bot.send_message(
            chat_id=user['id'],
            text=templates.wrong_command_message)
    config.Save()
    context.bot.send_message(
        chat_id=user['id'],
        text=templates.mute_status_on if user['mute'] else templates.mute_status_off)


def cmd_delay(update: Update, context):
    user, is_admin, is_moder = get_user_and_status(update)
    if is_admin:
        pass
    else:
        context.bot.send_message(
            chat_id=user['id'],
            text=templates.denied_message)


def cmd_cheer_up(update: Update, context):
    user, is_admin, is_moder = get_user_and_status(update)


# Other stuff


def main():
    # current_timestamp = int(time.time())  # начальное значение timestamp

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', cmd_add))
    dispatcher.add_handler(CommandHandler('mute', cmd_mute))
    dispatcher.add_handler(CommandHandler('delay', cmd_delay))
    dispatcher.add_handler(CommandHandler('cheer_up', cmd_cheer_up))
    updater.start_polling()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    while True:
        messages = config.data['messages']
        for user in TELEGRAM_USERS.values():
            id = user["id"]
            if user['mute']:
                print(f"User muted: {user['name']}")
                continue
            message = messages[random.randint(0, len(messages) - 1)]
            print(f'Sending message "{message}" to {id} {user["name"]}')
            bot.send_message(chat_id=id, text=message)
        time.sleep(config.data['global']['delay'])


if __name__ == '__main__':
    main()
