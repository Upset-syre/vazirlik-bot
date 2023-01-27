import telebot
API_TOKEN = '1659824015:AAGOuOD0t_KJWkRVZYCwtpnETBdVG02E7v0'


bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
# btn = ['asd','fsa','gg']

# def generate_keyboard(btns):
#     x = telebot.types.ReplyKeyboardMarkup()
#     for x in btns:
#         y = telebot.types.KeyboardButton(x)
#         x.add(x)
#     return x
# msg = [category.query.all()]

# def generate_message_handlers(msg):
#     for x in msg:
#         dp.register_message_handler(Text(x.name_uz))
#         def handler_of_categories():
#             pass
