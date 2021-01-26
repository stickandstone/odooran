#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]


from servises import gate_control as gate
import logging
# from uuid import uuid4
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


SECRET, IDD = open('secret.txt').read().split(',')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != int(IDD):
        update.message.reply_text('Доступ ограничен.')
    else:
        update.message.reply_text('''Привет! Это бот который контролирует гаражные ворота.
        Используй /click для управления.''')


# Глобальные значения которые описывают состояние двери.
position = 0
t0 = 0
gate_is_opening = True


def make_click(update: Update, context: CallbackContext) -> None:
    """Открывает или закрывает ворота и сообщает об это в телеграм"""

    if update.message.chat_id != int(IDD):
        update.message.reply_text('Go away!')
    else:
        global t0, position, gate_is_opening
        t0, position, gate_is_opening, message = gate.action(
            t0, position, gate_is_opening)
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
