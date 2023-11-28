import logging
import os
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from telegram import Bot

from dialogflow import detect_intent_texts
from tg_bot import VKLogsHandler


logger_vk = logging.getLogger('Bot_helper_vk')


def make_answer(event, vk_api):
    user_text = event.text
    user_id = event.user_id

    bot_answer = detect_intent_texts(user_id, user_text)
    if bot_answer:
        vk_api.messages.send(
            user_id=user_id,
            message=bot_answer,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TG_ADMIN_ID')
    bot = Bot(tg_token)

    vk_session = vk_api.VkApi(token=vk_token)

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger_vk.setLevel(logging.INFO)
    logger_vk.addHandler(VKLogsHandler(bot, chat_id))
    logger_vk.info('Bot_helper VK is running')

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                make_answer(event, vk_api)
    except Exception as error:
        logger_vk.error(f'Возникла ошибка в работе ВК бота: {error}')
