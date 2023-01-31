import json

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, storage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite_db
from keyboards import kb_client, button_case_ru, user_kb, user_kb_ru, uz1, ru1, button_case_uz, en1, user_kb_en, \
    button_case_en, kb_client_change, uz_sets, uz_confirm_change_name

storage = MemoryStorage()

bot = Bot(token='5858403936:AAErWVpB06Np3CQyrQpDhekvizyMbfjlu0U')
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    # await bot.set_webhook("https://87b9-188-113-208-110.in.ngrok.io")
    print('bot online')
    # sqlite_db.sql_start()
    sqlite_db.sqlalchemy_Start()
    handlers()
    handlers_ru()
    handlers_uz_kir()
    lang_handler()
    lang_change_handler()
    handlers_settings_first()
    handlers_settings()
    handlers_settings_changes()
    await sqlite_db.check_answer()
    # sqlite_db.create_user()


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    # try:
    print(type(message.from_user.id))
    await sqlite_db.check_user(message.from_user.id)
    # if sqlite_db.sql_read():
    # message.delete() udalit soobsheniye otpravlennoe polzovatelem
    # await message.delete()
    # except:
    #     await message.reply('Obsheniye s botom cherez ls: https://t.me/test010299')


status_lang = None


class Regist(StatesGroup):
    name = State()
    phone = State()
    ad = State()
    user_id = State()
    lang = State()
    category = State()
    change_name = State()
    change_phone = State()


@dp.message_handler(Text(startswith='мои обращения'))
async def my_apps_ru(message: types.Message):
    await sqlite_db.get_my_apps(message.from_user.id)


@dp.message_handler(Text(startswith='mening murojaatlarim'))
async def my_apps_ru(message: types.Message):
    await sqlite_db.get_my_apps(message.from_user.id)


@dp.message_handler(Text(startswith='менинг мурожатларим'))
async def my_apps_en(message: types.Message):
    await sqlite_db.get_my_apps(message.from_user.id)


@dp.message_handler(Text(startswith="o'zbekcha"))
async def uz(message: types.Message):
    kb = sqlite_db.cats_kb()
    await bot.send_message(message.from_user.id, 'tugmasini bosing', reply_markup=kb)


@dp.message_handler(Text(startswith="русский"))
async def ru(message: types.Message):
    kb = sqlite_db.cats_kb_ru()
    await bot.send_message(message.from_user.id, 'нажмите кнопку', reply_markup=kb)


@dp.message_handler(Text(startswith="о'збекча"))
async def en(message: types.Message):
    kb = sqlite_db.cats_kb_uz_kir()
    await bot.send_message(message.from_user.id, 'тугмасини босинг', reply_markup=kb)


@dp.message_handler(Text(startswith="murojaatingizni qoldiring"))
async def uz_command(message: types.Message):
    global status_lang
    status_lang = 'uz'
    step = 0
    kb = sqlite_db.cats_kb()
    await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
    await bot.send_message(message.from_user.id, 'tugmasini bosing', reply_markup=kb)
    # await message.delete()


@dp.message_handler(Text(startswith="оставьте ваше обращение"))
async def ru_command(message: types.Message):
    global status_lang
    status_lang = 'ru'
    step = 0
    kb = sqlite_db.cats_kb_ru()
    await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
    await bot.send_message(message.from_user.id, 'нажмите кнопку', reply_markup=kb)


@dp.message_handler(Text(startswith="мурожатингизни колдиринг"))
async def en_command(message: types.Message):
    global status_lang
    status_lang = 'uz_kir'
    step = 0
    kb = sqlite_db.cats_kb_uz_kir()
    await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
    await bot.send_message(message.from_user.id, 'тугмасини босинг', reply_markup=kb)


@dp.message_handler(Text(startswith="подтвердить"), state=None)
async def start_ru(message: types.Message, state: FSMContext):
    global status_lang
    status_lang = 'ru'
    step = 1
    if status_lang == 'ru':
        await sqlite_db.check1(message.from_user.id, state, message, Regist, status_lang, step, cat)


@dp.message_handler(Text(startswith="tasdiqlang"), state=None)
async def start_uz(message: types.Message, state: FSMContext):
    global status_lang
    status_lang = 'uz'
    step = 1
    if status_lang == 'uz':
        print(step)
        await sqlite_db.check1(message.from_user.id, state, message, Regist, status_lang, step, cat)


@dp.message_handler(Text(startswith="тасдикланг"), state=None)
async def start_en(message: types.Message, state: FSMContext):
    global status_lang
    status_lang = 'uz_kir'
    step = 1
    if status_lang == 'uz_kir':
        print(step)
        await sqlite_db.check1(message.from_user.id, state, message, Regist, status_lang, step, cat)


@dp.message_handler(state=Regist.name)
async def load_name(message: types.Message, state: FSMContext):
    step = 2

    if status_lang == 'uz':
        # async with state.proxy() as data:
        #     data['name'] = message.text
        # await sqlite_db.check1(message.from_user.id, state, message)

        async with state.proxy() as data:

            data['name'] = message.text
            object = tuple(data.values())
            print(object)
        if object[0] == 'bekor qilish':
            await state.finish()
            await bot.send_message(message.from_user.id, 'bekor qilish', reply_markup=kb_client)
            return None

        await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
        await Regist.next()
    if status_lang == 'ru':
        async with state.proxy() as data:
            data['name'] = message.text

            object = tuple(data.values())
            print(object)
        if object[0] == 'отмена':
            await state.finish()
            await bot.send_message(message.from_user.id, 'отмена', reply_markup=kb_client)

        await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
        await Regist.next()

    if status_lang == 'uz_kir':
        async with state.proxy() as data:
            data['name'] = message.text

        await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
        await Regist.next()


@dp.message_handler(state=Regist.phone)
async def load_phone(message: types.Message, state: FSMContext):
    step = 3
    if status_lang == 'uz':
        # async with state.proxy() as data:
        #     data['phone'] = message.text
        # await sqlite_db.check2(message.from_user.id, state, message, Regist)

        async with state.proxy() as data:
            data['phone'] = message.text
            await Regist.next()

        await sqlite_db.take_text(status_lang, step, message.from_user.id, message)
    if status_lang == 'ru':
        async with state.proxy() as data:
            data['phone'] = message.text
            await Regist.next()

        await sqlite_db.take_text(status_lang, step, message.from_user.id, message)

    if status_lang == 'uz_kir':
        async with state.proxy() as data:
            data['phone'] = message.text
            await Regist.next()

        await sqlite_db.take_text(status_lang, step, message.from_user.id, message)


@dp.message_handler(state=Regist.ad)
async def load_phone(message: types.Message, state: FSMContext):
    step = 4
    if status_lang == 'uz':
        async with state.proxy() as data:
            data['ad'] = message.text
            data['user_id'] = message.from_user.id
            data['lang'] = status_lang
            data['category'] = cat

        # await sqlite_db.sql_add_command(state)
        await sqlite_db.createUser(state, message.from_user.id)
        await state.finish()

        # await sqlite_db.sql_read(message)
        object = tuple(data.values())
        print(object)

        if object[4] == 'bekor qilish' or object[0] == 'bekor qilish':
            print(object[4])

            return ''

        await sqlite_db.sql_read2(message, status_lang, step)
        await bot.send_message(message.from_user.id, 'Asosiy menyu', reply_markup=user_kb)

    if status_lang == 'ru':
        async with state.proxy() as data:
            data['ad'] = message.text
            data['user_id'] = message.from_user.id
            data['lang'] = status_lang
            data['category'] = cat

        # await sqlite_db.sql_add_command(state)
        await sqlite_db.createUser(state, message.from_user.id)
        await state.finish()
        object = tuple(data.values())

        if object[4] == 'отмена' or object[0] == 'отмена':
            print(object[4])

            return ''
        # await sqlite_db.sql_read(message)
        await sqlite_db.sql_read2(message, status_lang, step)
        await bot.send_message(message.from_user.id, 'главное меню', reply_markup=user_kb_ru)

    if status_lang == 'uz_kir':
        async with state.proxy() as data:
            data['ad'] = message.text
            data['user_id'] = message.from_user.id
            data['lang'] = status_lang
            data['category'] = cat

        # await sqlite_db.sql_add_command(state)
        await sqlite_db.createUser(state, message.from_user.id)
        await state.finish()
        object = tuple(data.values())
        if object[4] == 'бекор килиш' or object[0] == 'бекор килиш':
            print(object[4])
            print('here4')

            return ''
        # await sqlite_db.sql_read(message)
        await sqlite_db.sql_read2(message, status_lang, step)
        await bot.send_message(message.from_user.id, 'Асосий меню', reply_markup=user_kb_en)


@dp.message_handler(commands=['xxx'], state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print('xxx')
    if current_state is None:
        print('pidr')
        return
    await state.finish()
    await message.reply('OK')


@dp.message_handler(Text(startswith='bekor qilish'))
async def uz_cancel(message: types.Message):
    await sqlite_db.check_for_cancel(message.from_user.id, status_lang)


@dp.message_handler(Text(startswith='отмена'))
async def ru_cancel(message: types.Message):
    await sqlite_db.check_for_cancel(message.from_user.id, status_lang)


@dp.message_handler(Text(startswith='бекор килиш'))
async def en_cancel(message: types.Message):
    await sqlite_db.check_for_cancel(message.from_user.id, status_lang)


def generate_kb_cats():
    kb_ls = []
    a = sqlite_db.all_cats_uz()
    print(a)
    for x in a:
        kb_ls.append(KeyboardButton(x))

    return kb_ls


def generate_kb_cats_ru():
    kb_ls = []
    a = sqlite_db.all_cats_ru()
    print(a)
    for x in a:
        kb_ls.append(KeyboardButton(x))

    return kb_ls


def generate_kb_cats_uz_kir():
    kb_ls = []
    a = sqlite_db.all_cats_uz_kir()
    for x in a:
        kb_ls.append(KeyboardButton(x))

    return kb_ls


def handlers():
    for x in sqlite_db.all_cats_uz():
        dp.register_message_handler(category_handler, Text(startswith=x))


def handlers_ru():
    for x in sqlite_db.all_cats_ru():
        dp.register_message_handler(category_handler_ru, Text(startswith=x))


def handlers_uz_kir():
    for x in sqlite_db.all_cats_uz_kir():
        dp.register_message_handler(category_handler_uz_kir, Text(startswith=x))


# a = types.KeyboardButton('d')
# ab= types.KeyboardButton('g')
# sr = ReplyKeyboardMarkup(resize_keyboard=True).add(a, ab)
async def category_handler(message: types.Message):
    global cat
    cat = message.text

    await bot.send_message(message.from_user.id, 'tugmasini bosing', reply_markup=button_case_uz)


async def category_handler_ru(message: types.Message):
    global cat
    cat = message.text

    await bot.send_message(message.from_user.id, 'нажмите кнопку', reply_markup=button_case_ru)


async def category_handler_uz_kir(message: types.Message):
    global cat
    cat = message.text

    await bot.send_message(message.from_user.id, 'тугмасини босинг', reply_markup=button_case_en)


def lang_handler():
    langs = ['change uz', 'change ru', 'change uz_kir']
    for i in langs:
        dp.register_message_handler(select_lang, Text(startswith=i))


def lang_change_handler():
    langs = ["change o'zbekcha", 'change русский', "change о'збекча"]
    for i in langs:
        dp.register_message_handler(change_lang, Text(startswith=i))


async def select_lang(message: types.Message):
    await bot.send_message(message.from_user.id, 'change', reply_markup=kb_client_change)


async def change_lang(message: types.Message):
    if message.text == "change o'zbekcha":
        await sqlite_db.change_lang(message.from_user.id, 'uz')
    if message.text == 'change русский':
        await sqlite_db.change_lang(message.from_user.id, 'ru')
    if message.text == "change о'збекча":
        print('here')
        await sqlite_db.change_lang(message.from_user.id, 'uz_kir')


def handlers_settings_first():
    ls = ['see my name']
    for x in ls:
        dp.register_message_handler(seeMyname, Text(startswith=x))


async def seeMyname(message: types.Message):
    await sqlite_db.sendMyName(message.from_user.id)


def handlers_settings():
    ls = ['settings']
    for x in ls:
        dp.register_message_handler(settings, Text(startswith=x))


async def settings(message: types.Message):
    await bot.send_message(message.from_user.id, 'settings', reply_markup=uz_sets)


def handlers_settings_changes():
    ls = ['change name', 'change phone']
    for x in ls:
        dp.register_message_handler(change_settings, Text(startswith=x))


async def change_settings(message: types.Message, state: FSMContext):
    print(1)
    if message.text == 'change name':
        await sqlite_db.changes(message.from_user.id, state, message, Regist, 'uz', 'change_name')
    if message.text == 'change phone':
        await sqlite_db.changes(message.from_user.id, state, message, Regist, 'uz', 'change_phone')
        


@dp.message_handler(state=Regist.change_name)
async def changeName(message: types.Message, state: FSMContext):
    print(3)
    sqlite_db.change_name(message.from_user.id, message.text)
    await state.finish()


@dp.message_handler(state=Regist.change_phone)
async def changePhone(message: types.Message, state: FSMContext):
    print(3)
    sqlite_db.change_phone(message.from_user.id, message.contact)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
