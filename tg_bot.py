import logging
import os

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from dialogflow import detect_intent_texts


logger = logging.getLogger('Bot_helper')


class TelegramLogsHandler(logging.Handler):

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
    try:
        bot_answer = detect_intent_texts(user_id, user_text)
        update.message.reply_text(bot_answer)
    except:
        update.message.reply_text('Не понимаю о чем речь, '
                                  'набери /help и я расскажу тебе о чем мы можем поговорить')


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
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Bot is running')

    try:
        updater.start_polling()
        updater.idle()
    except Exception as error:
        logger.error(f'Возникла ошибка при запуске бота: {error}')

