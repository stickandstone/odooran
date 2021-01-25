#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]


import sys
import time
import logging
from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    import test_relay as relay
else:
    import relay


SECRET, IDD = open('secret.txt').read().split(',')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != int(IDD):
        update.message.reply_text('Доступ ограничен.')
    else:
        update.message.reply_text('''Привет! Это одоран, бот который открывает гаражные ворота.
        Используй /click для открытия, остановки или закрытия двери.''')


# Глобальные значения которые описывают состояние двери.
position = 0
t0 = time.time()
gate_is_opening = True


def make_click(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != int(IDD):
        update.message.reply_text('Go away!')
    else:
        global t0, position, gate_is_opening
        t1 = time.time()
        if position != 0:
            if gate_is_opening:
                position = t0 - t1
            else:
                position = t1 - t0

        if position <= 0:
            message = 'Открываю ворота'
            position = 1
        elif position >= 25:
            message = 'Закрываю ворота'
            position = 24

        else:
            relay.click()
            if gate_is_opening:
                message = 'Открываю ворота'
            else:
                message = 'Закрываю ворота'

        gate_is_opening = not gate_is_opening
        t0 = t1
        relay.click()
        update.message.reply_text(message)


def main() -> None:
     updater = Updater(SECRET, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("click", make_click))
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
