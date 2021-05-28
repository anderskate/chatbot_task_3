# Bot assistant for employees
Helps answer user questions. Uses DialogFlow service with machine learning

For testing, you can use these bots:
In TG: @QwerfrhhyuuBot
In VK: https://vk.com/club204754660

# How to install
The script uses enviroment file with authorization data. The file '.env' must include following data:
- GOOGLE_APPLICATION_CREDENTIALS, credentials for google DialogFlow authorization
- DIALOGFLOW_PROJECT_ID, project id in DialogFlow service
- TELEGRAM_TOKEN, Telegram bot token
- VK_TOKEN, VK bot token
- TG_ADMIN_CHAT_ID, Telegram admin chat id for debugging

Python 3 should be already installed. Then use pip3 (or pip) to install dependencies:

```bash
pip3 install -r requirements.txt
```

# How to launch
The Example of launch tg and vk bots in Ubuntu is:

```bash
$ python3 tg_chat_bot.py
$ python3 vk_chat_bot.py
```

It is better to launch the script on a remote server, [Heroku](https://devcenter.heroku.com/articles/how-heroku-works), for example. It provides that it will work around the clock. A "Procfile" is need to launch correctly on Heroku.

# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org, module [Chat Bots with Python](https://dvmn.org/modules/chat-bots/lesson/devman-bot/#review-tabs).