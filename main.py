from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
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
        bot.send_message(
            chat_id=update.message.chat_id,
            text=update.message.text
        )

    def start_chat(self):
        self.updater.start_polling()


def main():
    """"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot_token = '1720558878:AAH-sE9uPV2rhs2VzURnX_0N6krP9NMxzuw'
    dialog_bot = DialogBot(bot_token)
    dialog_bot.start_chat()


if __name__ == '__main__':
    main()
