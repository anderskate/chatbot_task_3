import os
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from dotenv import load_dotenv
from dialogflow_services import detect_intent_texts
from logs_handler import LogsHandler


logger = logging.getLogger(__file__)


class DialogTelegramBot:
    """Telegram bot assistant.

    This bot helps to answer frequently asked questions of users.
    """
    def __init__(self, token):
        """Initialize TelegramBot instance."""
        self.project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

        self.updater = Updater(token=token)

        start_handler = CommandHandler(
            'start', self.start
        )
        self.updater.dispatcher.add_handler(start_handler)

        message_reply_handler = MessageHandler(
            Filters.text, self.reply_to_message
        )
        self.updater.dispatcher.add_handler(message_reply_handler)

    def start(self, bot, update):
        """Handle start command from user."""
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Здравствуйте!"
        )

    def reply_to_message(self, bot, update):
        """Reply to message for user question using DialogFlow."""
        user_text = update.message.text
        user_id = update.message.chat_id
        language_code = 'ru'
        bot_response, _ = detect_intent_texts(
            self.project_id, user_id,
            user_text, language_code
        )

        bot.send_message(
            chat_id=update.message.chat_id,
            text=bot_response,
        )

    def start_bot(self):
        """Start chat bot."""
        self.updater.start_polling()


def main():
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logs_handler = LogsHandler(level=logging.INFO)
    logger.addHandler(logs_handler)

    bot_token = os.getenv('TELEGRAM_TOKEN')
    dialog_bot = DialogTelegramBot(bot_token)
    dialog_bot.start_bot()


if __name__ == '__main__':
    main()
