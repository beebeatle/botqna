# import everything
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Hi, I'm a Good Mood bot. What's your name?
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

   else:
       bot_other="Nice to meet you, "+text+"! Happy Holidays!"
       bot.sendMessage(chat_id=chat_id, text=bot_other, reply_to_message_id=msg_id)

   return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/test', methods=['GET', 'POST'])
def set_test():
    return 'Test ok'


@app.route('/')
def index():
    return 'Hi!'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)