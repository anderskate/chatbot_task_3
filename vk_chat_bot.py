import random
import os
import logging

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from utils import detect_intent_texts
from logs_handler import LogsHandler
from dotenv import load_dotenv


logger = logging.getLogger(__file__)


class DialogVKBot:
    """VK bot assistant.

    This bot helps to answer frequently asked questions of users.
    """
    def __init__(self):
        """Initialize VKBot instance."""
        self.project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        self.vk_group_token = os.getenv('VK_TOKEN')

    def echo(self, event, vk_api):
        """Handle user question using DialogFlow."""

        session_id = event.user_id

        message_response = detect_intent_texts(
            self.project_id, session_id,
            event.text, 'ru',
        )
        if not message_response:
            return

        vk_api.messages.send(
            user_id=session_id,
            message=message_response,
            random_id=random.randint(1,1000)
        )

    def start_chat(self):
        """Start chat bot."""
        vk_session = vk.VkApi(token=self.vk_group_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                try:
                    self.echo(event, vk_api)
                except Exception as e:
                    logger.exception(e)


def main():
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logs_handler = LogsHandler(level=logging.INFO)
    logger.addHandler(logs_handler)
    vk_chat_bot = DialogVKBot()
    vk_chat_bot.start_chat()


if __name__ == "__main__":
    main()
