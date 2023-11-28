import json
import os

from dotenv import load_dotenv


load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LANGUAGE = os.getenv('LANGUAGE_CODE')


def create_intent(display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(PROJECT_ID)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(request={"parent": parent, "intent": intent})


def detect_intent_texts(session_id, text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    try:
        text_input = dialogflow.TextInput(text=text, language_code=LANGUAGE)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return response.query_result.fulfillment_text

    except response.query_result.intent.is_fallback:
        return None


if __name__ == '__main__':
    with open('questions.json', 'r') as json_file:
        user_requests = json.load(json_file)
        for user_request in user_requests:
            try:
                name = user_request
                phrases = user_requests[user_request]['questions']
                answer = [user_requests[user_request]['answer']]
                create_intent(name, phrases, answer)
                print(f'Запись "{name}" добавлена успешно')
            except Exception as error:
                print(f'При добавлении записи "{name}" возникла ошибка: {error}')