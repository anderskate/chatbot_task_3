import os
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from dotenv import load_dotenv
from utils import detect_intent_texts


class DialogTelegramBot:
    """Telegram bot assistant.

    This bot helps to answer frequently asked questions of users.
    """
    def __init__(self, token):
        """Initialize TelegramBot instance."""
        self.project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        self.session_id = os.getenv('DIALOGFLOW_SESSION_ID')

        self.updater = Updater(token=token)

        start_handler = CommandHandler('start', self.start)
        self.updater.dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text, self.echo)
        self.updater.dispatcher.add_handler(echo_handler)

    def start(self, bot, update):
        """Handle start command from user."""
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Здравствуйте!"
        )

    def echo(self, bot, update):
        """Handle user question using DialogFlow."""
        user_text = update.message.text
        language_code = 'ru'
        bot_response = detect_intent_texts(
            self.project_id, self.session_id,
            user_text, language_code
        )

        bot.send_message(
            chat_id=update.message.chat_id,
            text=bot_response,
        )

    def start_chat(self):
        """Start chat bot."""
        self.updater.start_polling()


def main():
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot_token = os.getenv('TELEGRAM_TOKEN')
    dialog_bot = DialogTelegramBot(bot_token)
    dialog_bot.start_chat()


if __name__ == '__main__':
    main()
