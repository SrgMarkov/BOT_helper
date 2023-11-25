import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LANGUAGE = os.getenv("LANGUAGE_CODE")


bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ твой бот помощник!\nЗадай мне вопрос')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Помогу тебе с самыми важными вопросами'
    )


@dp.message()
async def send_echo(message: Message):
    user_message = message.text
    chat_id = message.chat.id
    bot_answer = detect_intent_texts(PROJECT_ID, chat_id, user_message, LANGUAGE)
    await message.reply(text=bot_answer)


if __name__ == '__main__':
    dp.run_polling(bot)
