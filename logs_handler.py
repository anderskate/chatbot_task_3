import logging
import telegram
import os


class LogsHandler(logging.Handler):
    """Log handler that redirects log messages to telegram chat."""
    def __init__(self, level):
        self.bot_token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TG_ADMIN_CHAT_ID')
        self.bot = telegram.Bot(token=self.bot_token)
        super().__init__(level)

    def emit(self, record):
        """Get formatting log message and send it to telegram chat."""
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)