import logging
import os

import telegram.error
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from dialogflow import detect_intent_texts


logger_tg = logging.getLogger('Bot_helper_tg')


class BotLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context) -> None:
    update.message.reply_text(
        'Привет! Я твой бот помощник. Задай мне вопрос'
    )


def help_handler(update: Update, context) -> None:
    update.message.reply_text(
        '''На данные момент я могу отвечать на следующие вопросы:
        - Вопросы от действующих партнёров
        - Вопросы от забаненных
        - Забыл пароль
        - Удаление аккаунта
        - Устройство на работу
        А так же могу с тобой поздороваться) '''
    )


def make_answer(update, context) -> None:
    user_text = update.message.text
    user_id = update.message.from_user.id
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    language = os.getenv('LANGUAGE_CODE')
    bot_answer = detect_intent_texts(user_id, user_text, project_id, language)
    update.message.reply_text(bot_answer.query_result.fulfillment_text)


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TG_ADMIN_ID')
    bot = Bot(tg_token)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, make_answer))

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger_tg.setLevel(logging.INFO)
    logger_tg.addHandler(BotLogsHandler(bot, chat_id))
    logger_tg.info('Bot_helper TG is running')

    try:
        updater.start_polling()
        updater.idle()
    except Exception as error:
        logger_tg.error(f'Возникла ошибка в работе бота: {error}')

