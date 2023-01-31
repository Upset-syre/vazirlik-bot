import sqlite3 as sq
import psycopg2 as sq
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# from aiogram.types import message

from bot_tg import bot, generate_kb_cats, generate_kb_cats_ru, generate_kb_cats_uz_kir
from keyboards import kb_client, user_kb, user_kb_ru, user_kb_en, uz_sets_change


def sql_start():
    global base, cur
    base = sq.connect(database="vazirlik_bot",
                      host="127.0.0.1",
                      user="postgres",
                      password="admin",
                      port="5432")
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    data = [
        "CREATE TABLE IF NOT EXISTS application (id SERIAL PRIMARY KEY, name TEXT, phone TEXT , application TEXT, status TEXT DEFAULT 'false', user_id INT, answer TEXT NULL)",
        "CREATE TABLE IF NOT EXIST "]
    cur.executemany()
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        result = tuple(data.values())
        print(result)
        cur.execute(f'INSERT INTO application (name, phone, application, user_id) VALUES (%s, %s, %s, %s)', result)
        base.commit()


async def sql_read(message):
    print(message.from_user.id)
    cur.execute("SELECT id FROM application;")
    ls = []
    for i in cur.fetchall():
        ls.append(i[0])
    await message.reply(f'''Hurmatli murojaatchi sizning murojaatingiz qabul qilindi.
Sizning tartib raqamingiz №{ls[-1]} 
''')


from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    fio = Column('fio', String)
    phone = Column('phone', String)
    lang = Column('lang', String)
    tg_user_id = Column('tg_user_id', Integer)
    application = relationship("Application", backref='users')

    def __init__(self, fio, phone, tg_user_id, lang):
        self.fio = fio
        self.phone = phone
        self.tg_user_id = tg_user_id
        self.lang = lang

    def __repr__(self):
        return f"{self.id}"


class Category(Base):
    __tablename__ = 'category'
    id = Column('id', Integer, primary_key=True)
    name_uz = Column('name_uz', String, unique=True)
    name_ru = Column('name_ru', String, unique=True)
    name_uz_kir = Column('name_uz_kir', String, unique=True)
    application = relationship("Application", backref='categories')

    def __init__(self, name_uz, name_ru, name_uz_kir):
        self.name_uz = name_uz
        self.name_ru = name_ru
        self.name_uz_kir = name_uz_kir


class Application(Base):
    __tablename__ = 'application'
    id = Column('id', Integer, primary_key=True)
    status = Column('status', String, default='pending')
    application = Column('application', Text, default='pending')
    answer = Column('answer', String)
    sent = Column('sent', String)
    lang = Column('lang', String)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    def __int__(self, status, application, answer, user_id, category_id, sent):
        self.status = status
        self.application = application
        self.answer = answer
        self.user_id = user_id
        self.category_id = category_id
        self.sent = sent


class Text(Base):
    __tablename__ = 'text'
    id = Column('id', Integer, primary_key=True)
    greeting = Column('greeting', Text)
    step1 = Column('step1', String)
    step2 = Column('step2', String)
    step3 = Column('step3', Text)
    step4 = Column('step4', Text)
    lang = Column('lang', Text)

    def __int__(self, id, greeting, step1, step2, step3, step4, lang):
        self.id = id
        self.greeting = greeting
        self.step1 = step1
        self.step2 = step2
        self.step3 = step3
        self.step4 = step4
        self.lang = lang


async def take_text(lang, step, user_id, message, ls=None):
    text = session.query(Text).filter_by(lang=lang).first()
    # user = session.query(User).filter_by(tg_user_id=user_id).first()

    if step == 0:
        await bot.send_message(user_id, text.greeting)

    if step == 1:
        await bot.send_message(user_id, text.step1, )
    if step == 2:
        await bot.send_message(user_id, text.step2)
    if step == 3:
        await bot.send_message(user_id, text.step3)
    if step == 4:
        await bot.send_message(user_id, text.step4 + ls)


def sqlalchemy_Start():
    global session
    engine = create_engine("postgresql://postgres:admin@localhost:5432/vazirlik_bot", echo=False)

    if engine:
        print('Base connected!')
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()






def cats_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,  row_width=1, one_time_keyboard=True).add(*generate_kb_cats())
    return kb

def cats_kb_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,  row_width=1, one_time_keyboard=True).add(*generate_kb_cats_ru())
    return kb

def cats_kb_uz_kir():
    kb = ReplyKeyboardMarkup(resize_keyboard=True,  row_width=1, one_time_keyboard=True).add(*generate_kb_cats_uz_kir())
    return kb

def create_user():
    user = User(fio='sarik', phone='565545565', tg_user_id=544845412)

    session.add(user)
    session.commit()


async def createUser(state, user_id):
    user = session.query(User).filter_by(tg_user_id=user_id).first()
    async with state.proxy() as data:
        object = tuple(data.values())
        print(object)

        if object[4] == 'cancel' or object[0] == 'cancel':
            print(object[4])
            print('here')
            await bot.send_message(user_id, 'cancel', reply_markup=user_kb_en)
            return ''

        if object[4] == 'отмена' or object[0] == 'отмена':
            print(object[4])
            await bot.send_message(user_id, 'отмена', reply_markup=user_kb_ru)
            return ''

        if object[4] == 'bekor qilish' or object[0] == 'bekor qilish':
            print(object[4])
            await bot.send_message(user_id, 'bekor qilish', reply_markup=user_kb)
            return ''

        else:

            if user:
                if object[2] == 'uz':
                    cat = session.query(Category).filter_by(name_uz=object[3]).first()
                if object[2] == 'ru':
                    cat = session.query(Category).filter_by(name_ru=object[3]).first()
                if object[2] == 'uz_kir':
                    cat = session.query(Category).filter_by(name_uz_kir=object[3]).first()

                print(object)
                app = Application(application=object[4], user_id=user.id, category_id=cat.id, lang=object[2])

                session.add(app)
                session.commit()



            else:

                if object[4] == 'uz':
                    cat = session.query(Category).filter_by(name_uz=object[5]).first()
                if object[4] == 'ru':
                    cat = session.query(Category).filter_by(name_ru=object[5]).first()
                if object[4] == 'uz_kir':
                    cat = session.query(Category).filter_by(name_uz_kir=object[5]).first()

                print(object)
                user = User(fio=object[0], phone=object[1], tg_user_id=object[3], lang=object[4])
                session.add(user)
                session.flush()

                app = Application(application=object[2], user_id=user.id, category_id=cat.id, lang=object[4])

                session.add_all([user, app])
                session.commit()


async def sql_read2(message, lang, step):
    print(message.from_user.id)
    app = session.query(Application.id).join(User, User.id == Application.user_id).filter(
        User.tg_user_id == message.from_user.id).all()
    ls = []

    for i in app:
        ls.append(i[0])
    await take_text(lang, step, message.from_user.id, message, str(ls[-1]))


async def check_user(user_id):
    global user_tg
    try:
        user = session.query(User).filter_by(tg_user_id=user_id).first()


        user_tg = user.tg_user_id
        if user:
            print('User')
            if user.lang == 'uz':
                await bot.send_message(user_id, 'Qishloq xo‘jaligi vazirligiga Xush kelibsiz!', reply_markup=user_kb)
            if user.lang == 'ru':
                await bot.send_message(user_id, 'Добро пожаловать в Министерство сельского хозяйства!',
                                       reply_markup=user_kb_ru)
            if user.lang == 'uz_kir':
                await bot.send_message(user_id, 'Қишлоқ ҳужалиги вазирлигига ҳуш келибсиз!',
                                       reply_markup=user_kb_en)
    except:
        print(user_id)
        print('No user')
        await bot.send_message(user_id, 'Qishloq xo‘jaligi vazirligiga Xush kelibsiz!', reply_markup=kb_client)


async def get_my_apps(user_id):
    apps = session.query(Application).join(User, User.id == Application.user_id).filter(
        User.tg_user_id == user_id).order_by(Application.id)

    for i in apps:
        if i.users.lang == 'uz':
            await bot.send_message(user_id,
                                   f'''№{i.id} \ncategoriya: {i.categories.name_uz} \nsizning murojaatingiz: {i.application} \ndavolash murojaati: {i.status} \nso'rovga javob: {i.answer if i.answer != None else ''}
                                ''')

        if i.users.lang == 'ru':
            await bot.send_message(user_id,
                                   f'''№{i.id} \ncategoriya: {i.categories.name_ru} \nваше обращение: {i.application} \nстатус обращения: {i.status} \nответ на обращение: {i.answer if i.answer != None else ''}
                     ''')

        if i.users.lang == 'uz_kir':
            await bot.send_message(user_id,
                                   f'''№{i.id} \ncategoriya: {i.categories.name_uz_kir} \nyour application: {i.application} \nstatus of application: {i.status} \nanswer on application: {i.answer if i.answer != None else ''}
                     ''')


async def check1(user_id, state, message, Regist, lang, step, cat):
    user = session.query(User).filter_by(tg_user_id=user_id).first()
    if user:
        await Regist.ad.set()
        async with state.proxy() as data:
            data['name'] = user.fio
            data['phone'] = user.phone
            data['lang'] = lang
            data['category'] = cat
            await take_text(lang, 3, message.from_user.id, message)

    else:
        await take_text(lang, step, message.from_user.id, message)
        await Regist.name.set()

async def changes(user_id, state, message, Regist, lang, step):

    if step == 'change_name':
        print(2)
        await Regist.change_name.set()
        async with state.proxy() as data:
            data['change_name'] = message.text
            await take_text(lang, 1,user_id, message)
    if step == 'change_phone':
        print(2)
        await Regist.change_phone.set()
        async with state.proxy() as data:
            data['change_phone'] = message.text
            await take_text(lang, 2,user_id, message)



async def check2(user_id, state, message, Regist):
    user = session.query(User).filter_by(tg_user_id=user_id).first()
    if user:
        async with state.proxy() as data:
            data['phone'] = user.phone


def all_cats_uz():
    cats = session.query(Category).all()

    ls = []
    for cat in cats:
        ls.append(cat.name_uz)
    return ls

def all_cats_ru():
    cats = session.query(Category).all()

    ls = []
    for cat in cats:
        ls.append(cat.name_ru)
    return ls

def all_cats_uz_kir():
    cats = session.query(Category).all()

    ls = []
    for cat in cats:
        ls.append(cat.name_uz_kir)
    return ls


async def send_message():
    apps = session.query(Application.answer).join(User, User.id == Application.user_id).filter(
        User.tg_user_id == user_tg).all()

    if apps:
        await bot.send_message(user_tg, apps[-1])


async def check_for_cancel(user_id, lang):

    user = session.query(User).filter_by(tg_user_id=user_id).first()

    if user:
        if lang == 'uz' or user.lang == 'uz':
            await bot.send_message(user_id, 'bekor qilish', reply_markup=user_kb)
        if lang == 'ru' or user.lang == 'ru':
            await bot.send_message(user_id, 'отмена', reply_markup=user_kb_ru)
        if lang == 'uz_kir' or user.lang == 'uz_kir':
            await bot.send_message(user_id, 'бекор килиш', reply_markup=user_kb_en)

    else:

        if lang == 'uz':
            await bot.send_message(user_id, 'bekor qilish', reply_markup=kb_client)
        if lang == 'ru':
            await bot.send_message(user_id, 'отмена', reply_markup=kb_client)
        if lang == 'uz_kir':
            await bot.send_message(user_id, 'бекор килиш', reply_markup=kb_client)


async def check_answer():
    applications = session.query(Application).all()

    for i in applications:
        if i.answer != None and i.sent == None:
            i.sent = 'sent'

            session.commit()

            await bot.send_message(i.users.tg_user_id, i.answer,allow_sending_without_reply=True)



async def change_lang(user_id, lang):
    user = session.query(User).filter_by(tg_user_id=user_id).first()

    user.lang = lang

    session.commit()

    if lang == 'uz':
        await bot.send_message(user_id, '1', reply_markup=user_kb)

    if lang == 'ru':
        await bot.send_message(user_id, '1', reply_markup=user_kb_ru)

    if lang == 'uz_kir':
        await bot.send_message(user_id, '1', reply_markup=user_kb_en)


def change_name(user_id, new_name):
    user = session.query(User).filter_by(tg_user_id=user_id).first()
    print('ssss')
    user.fio = new_name
    session.commit()


def change_phone(user_id, new_phone):
    user = session.query(User).filter_by(tg_user_id=user_id).first()

    user.phone = new_phone
    session.commit()


async def sendMyName(user_id):
    user = session.query(User).filter_by(tg_user_id=user_id).first()
    await bot.send_message(user_id, f'your name {user.fio}, your phone: {user.phone}', reply_markup=uz_sets_change)

async def sendMyPhone(user_id):
    user = session.query(User).filter_by(tg_user_id=user_id).first()
    await bot.send_message(user_id, f'your phone {user.phone}', reply_markup=uz_sets_change)