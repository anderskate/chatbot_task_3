import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from google.cloud import dialogflow


def echo(event, vk_api):
    project_id = ''
    session_id = event.user_id

    message_response = detect_intent_texts(
        project_id, session_id,
        event.text, 'ru',
    )
    if not message_response:
        return

    vk_api.messages.send(
        user_id=session_id,
        message=message_response,
        random_id=random.randint(1,1000)
    )


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))


    text_input = dialogflow.TextInput(
        text=text,
        language_code=language_code,
    )

    query_input = dialogflow.QueryInput(
        text=text_input
    )

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(
        response.query_result.fulfillment_text))

    if response.query_result.intent.is_fallback:
        return

    return response.query_result.fulfillment_text


if __name__ == "__main__":
    vk_group_token = ''
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
