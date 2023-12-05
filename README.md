# Умный бот помощник в ВК и Telegram

Telegram и ВК бот для получения консультации пользователей. Бот обучается нейросетью dialogflow

### Пример работы

![demo_tg_bot](https://github.com/SrgMarkov/BOT_helper/assets/107784915/d18ae87a-bfc1-4664-afbd-a80c60624333)

![demo_vk_bot](https://github.com/SrgMarkov/BOT_helper/assets/107784915/8ebea056-003e-4fb8-82f7-d52a80ba0503)


### Необходимые требования

1. Настроенный бот dialogflow ES ([Документация](https://cloud.google.com/dialogflow/es/docs/basics))
2. Токен телеграм бота ([Как создать канал, бота и получить токен](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/))
3. Токен группы ВК



### Как установить

- Python3 должен быть уже установлен, виртуальное окружение для проекта скопировано и активировано.
- в директории с файлами программы необходимо создать `.env` файл, в котором прописать токены и Ваш персональный chat_id TG(можно получить, написав боту [@userinfobot](https://telegram.me/userinfobot)), а так же настройки dialogflow в формате `ТОКЕН=значение`
```
TELEGRAM_BOT_TOKEN - токен телеграм
VK_TOKEN - токен ВК
TG_ADMIN_ID - ид чата TG для уведомлений
GOOGLE_APPLICATION_CREDENTIALS - путь до файла application_default_credentials.json
GOOGLE_CLOUD_PROJECT - id проекта dialogflow
LANGUAGE_CODE - язык бота
QUESTIONS_FILE - путь к файлу с вопросами
```
Установить зависимости командой
```bash
pip install -r requirements.txt
```
### Как запустить

Запустить скрипты командами:
```bash
python3 tg_bot.py
```
```bash
python3 vk_bot.py
```

### Обучение бота

Для обучения бота необходимо подготовить json файл с вопросами в формате
```json
"название": {
        "questions": [
            "вопрос 1",
            "Вопрос 2",
            ...        
            "Здесь должны быть все возможные вопросы от пользователей"
        ],
        "answer": "Ответ бота"
```
Указать путь до файла с вопросами в `.env`, например:
```
QUESTIONS_FILE=/Users/Username/Documents/questions.json
```

Запустить скрипт
```bash
python3 dialogflow.py
```
При этом в терминал выведутся сообщения о успешности / неуспешности загрузки вопросов
