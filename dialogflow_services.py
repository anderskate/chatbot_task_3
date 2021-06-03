from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent from with texts as inputs
    and is the text fallback or not.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

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

    text_result = response.query_result.fulfillment_text
    text_is_fallback = False

    if response.query_result.intent.is_fallback:
        text_is_fallback = True

    return text_result, text_is_fallback
