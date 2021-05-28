import json
import os
from google.cloud import dialogflow
from dotenv import load_dotenv


# Data JSON file with intent questions
INTENT_QUESTIONS_FILE = 'chat_questions.json'


def get_data_from_file(file_path):
    """Get data from JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def create_intent(
        project_id, display_name,
        training_phrases_parts, message_texts
):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])

    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    agents_client = dialogflow.AgentsClient()
    agents_client.train_agent(parent=f'projects/{project_id}')


def main():
    load_dotenv()
    data = get_data_from_file(INTENT_QUESTIONS_FILE)
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    for intent_key, intent_data in data.items():
        create_intent(
            project_id, intent_key,
            intent_data['questions'],
            intent_data['answer'],
        )


if __name__ == '__main__':
    main()
