#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

import logging
from uuid import uuid4

# from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, KeyboardButton
# from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
# from telegram.utils.helpers import escape_markdown


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


import sys

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    pass
else:
    import relay


SECRET = open('secret.txt').read()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

gate_is_close = True
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('''Привет! Это одоран, бот который открывает гаражные ворота. 
    Используй /click для открытия, остановки или закрытия двери.''')

    test_text = 'Open the gate!'

    keyboard = [
        [
            InlineKeyboardButton(test_text, callback_data='1')
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def make_click(update: Update, context: CallbackContext) -> None:
    global gate_is_close

    if gate_is_close:
        update.message.reply_text('Открываю дверь...')
    else:
        update.message.reply_text('Закрываю дверь...')

    gate_is_close = not gate_is_close

    relay.click()


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def main() -> None:
    updater = Updater(SECRET, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("click", make_click))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
