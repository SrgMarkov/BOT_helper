import json
import os

from dotenv import load_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

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


if __name__ == '__main__':
    load_dotenv()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    with open('questions.json', 'r') as json_file:
        user_requests = json.load(json_file)
        for user_request in user_requests:
            try:
                name = user_request
                phrases = user_requests[user_request]['questions']
                answer = [user_requests[user_request]['answer']]
                create_intent(project_id, name, phrases, answer)
                print(f'Запись "{name}" добавлена успешно')
            except Exception as error:
                print(f'При добавлении записи "{name}" возникла ошибка: {error}')
