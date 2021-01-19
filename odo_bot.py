#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]


import sys
import time
import logging
from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    pass
else:
    import relay


SECRET, IDD = open('secret.txt').read().split(',')
print(SECRET)
print(IDD)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Глобальные значения, которые описывают состояние двери.
gate_is_close = True
TIME_TO_OPEN = 20
past_click_time = 0

def start(update: Update, context: CallbackContext) -> None:
    idd = update.message.chat_id
    print(idd)
    if idd != int(IDD):
        update.message.reply_text('Доступ ограничен.')
    else:
        update.message.reply_text('''Привет! Это одоран, бот который открывает гаражные ворота. 
        Используй /click для открытия, остановки или закрытия двери.''')
        # Осталось кнопка, промежуточное состояние ворот откр\закр, проверить безопасность, оформить репо
    
def make_click(update: Update, context: CallbackContext) -> None:
    idd = update.message.chat_id
    if idd != int(IDD):
        update.message.reply_text('Go away!')
    else:
        global gate_is_close, past_click_time

        time_between_ckicks = time.time() - past_click_time
        past_click_time = time.time()
        gate_is_moving = time_between_ckicks < TIME_TO_OPEN
        
        if gate_is_moving:
            relay.click()

        if gate_is_close:
            update.message.reply_text('⬆️⬆️⬆️Открываю ворота⬆️⬆️⬆️')
            relay.click()

        else:
            update.message.reply_text('⬇️⬇️⬇️Закрываю ворота⬇️⬇️⬇️')
            relay.click()

        gate_is_close = not gate_is_close

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
