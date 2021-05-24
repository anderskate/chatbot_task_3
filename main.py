from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from google.cloud import dialogflow
import logging


class DialogBot:
    def __init__(self, token):
        """"""
        self.updater = Updater(token=token)

        start_handler = CommandHandler('start', self.start)
        self.updater.dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text, self.echo)
        self.updater.dispatcher.add_handler(echo_handler)

    def start(self, bot, update):
        """"""
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Здравствуйте!"
        )

    def echo(self, bot, update):
        """"""
        project_id = 'tactical-codex-313718'
        session_id = 590772216
        user_text = update.message.text
        language_code = 'ru'
        bot_response = self.detect_intent_texts(
            project_id, session_id,
            user_text, language_code
        )

        bot.send_message(
            chat_id=update.message.chat_id,
            text=bot_response,
        )

    def detect_intent_texts(self, project_id, session_id, text, language_code):
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

        return response.query_result.fulfillment_text

    def start_chat(self):
        self.updater.start_polling()


def main():
    """"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot_token = ''
    dialog_bot = DialogBot(bot_token)
    dialog_bot.start_chat()


if __name__ == '__main__':
    main()
