#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]


from servises import gate_control as gate
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import json

with open('secret.json') as conf_file:
    conf = json.load(conf_file)

TOKEN = conf['TOKEN']
IDD = conf['CHAT_ID']

gate_state_global = {
    "pos": 0,
    "t0": 0,
    "gio": True,
    "msg": ""
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != int(IDD):
        update.message.reply_text('Доступ ограничен.')
    else:
        update.message.reply_text('''Это бот для контроля гаражных ворот.
        Используй /click для управления.''')


def make_click(update: Update, context: CallbackContext) -> None:
    """turns the relay on and sends a telegram message"""

    if update.message.chat_id != int(IDD):
        update.message.reply_text('Go away!')
    else:
        global gate_state_global
        gate_state_global = gate.action(gate_state_global)
        update.message.reply_text(gate_state_global["msg"])


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("click", make_click))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
