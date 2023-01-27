from flask import *
import requests
from json import loads
from app.core import token_required
from telebot import types,TeleBot
from flask_login import login_required
from app.models import *
# API_TOKEN = '1659824015:AAGOuOD0t_KJWkRVZYCwtpnETBdVG02E7v0'

# bot = TeleBot(API_TOKEN)

# bot_blueprint = Blueprint('tgbot', __name__, url_prefix='/tgbot')

# @bot_blueprint.route("/", methods = ['GET','POST'])
# def tgbot():
#     if request.method == "POST":
#         result = request.body.decode("utf-8")
#         update = types.Update.de_json(loads(result))
#         bot.process_new_updates([update])

#         return jsonify({"g":'s'})
#     return jsonify(requests.get("https://api.telegram.org/bot%s/getMe" % bot.token).json(), status=200)


home = Blueprint("home", __name__, url_prefix='/home')

@home.route("/",methods = ['GET', 'POST'])
@login_required
def home_page():
    return render_template('dashboard.html')


@home.route("/login",methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        pass
    

    form = LoginForm()
    return render_template('signin.html',form = form)

    


# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message, """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """)


# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)

