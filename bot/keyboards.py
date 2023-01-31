from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("o'zbekcha")
b2 = KeyboardButton('русский')
b3 = KeyboardButton("о'збекча")
# b4 = KeyboardButton('uz_kir')

c1 = KeyboardButton("change o'zbekcha")
c2 = KeyboardButton('change русский')
c3 = KeyboardButton("change о'збекча")


'''Cancel'''
cancel_ru = KeyboardButton('отмена')
cancel_uz = KeyboardButton('bekor qilish')
cancel_en = KeyboardButton('бекор килиш')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3)

kb_client_change= ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(c1).add(c2).add(c3)


button_load_ru = KeyboardButton('подтвердить')
button_case_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_load_ru).add(cancel_ru)

button_load_uz = KeyboardButton('tasdiqlang')
button_case_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_load_uz).add(cancel_uz)

button_load_en = KeyboardButton('тасдикланг')
button_case_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_load_en).add(cancel_en)





my_apps_ru = KeyboardButton('мои обращения')
my_apps_uz = KeyboardButton('mening murojaatlarim')
my_apps_en = KeyboardButton('менинг мурожатларимs')
uz = KeyboardButton('uz')
ru = KeyboardButton('ru')
uz_1 = KeyboardButton('murojaatingizni qoldiring')
ru_1 = KeyboardButton('оставьте ваше обращение')
en_1 = KeyboardButton('мурожатингизни колдиринг')



user_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(my_apps_uz).add(uz_1).add(KeyboardButton('change uz')).add(KeyboardButton('settings'))
user_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(my_apps_ru).add(ru_1).add(KeyboardButton('change ru')).add(KeyboardButton('settings'))
user_kb_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(my_apps_en).add(en_1).add(KeyboardButton('change uz_kir')).add(KeyboardButton('settings'))



uz1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(uz_1)
ru1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(ru_1)
en1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(en_1)



'''Settings'''

uz_sets = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('see my name'))
uz_sets_change = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('change name')).add(KeyboardButton('change phone')).add(cancel_uz)


'''confirm changes'''
uz_confirm_change_name = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('confirm change'))