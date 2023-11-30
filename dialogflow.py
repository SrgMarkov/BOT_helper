import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(display_name, training_phrases_parts, message_texts, project_id):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
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


def detect_intent_texts(session_id, text, project_id, language):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    try:
        text_input = dialogflow.TextInput(text=text, language_code=language)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return response.query_result.fulfillment_text

    except response.query_result.intent.is_fallback:
        return None


if __name__ == '__main__':

    with open('questions.json', 'r') as json_file:
        load_dotenv()
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        user_requests = json.load(json_file)
        for user_request in user_requests:
            try:
                name = user_request
                phrases = user_requests[user_request]['questions']
                answer = [user_requests[user_request]['answer']]
                create_intent(name, phrases, answer, project_id)
                print(f'Запись "{name}" добавлена успешно')
            except Exception as error:
                print(f'При добавлении записи "{name}" возникла ошибка: {error}')