from app import db
from sqlalchemy.orm import relationship
import datetime
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms.validators import InputRequired, Length, ValidationError,DataRequired
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()], render_kw = {'placeholder' : 'Login'})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    style={'class': 'loginform', 'style': 'margin-top:12px'}

    submit = SubmitField("Sign in",render_kw = style)


class SendAnswerForm(FlaskForm):
    style_ = {'style': 'min-height: 200px',
    'placeholder' : 'Javob'
    }

    answer = TextAreaField(validators=[DataRequired()], render_kw = style_)
    

    style={'class': 'loginform', 'style': 'margin-top:12px'}

    submit = SubmitField("Jo'natish",render_kw = style)



class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseModel, db.Model):
    __tablename__ = 'user'
    fio = db.Column('fio', db.String)
    phone = db.Column('phone', db.String)
    lang = db.Column('lang', db.String)
    tuman_id = db.Column('tuman_id', db.Integer, db.ForeignKey('tuman.id'))
    mfy_id = db.Column('mfy_id', db.Integer, db.ForeignKey('mfy.id'))
    sex = db.Column('sex', db.String)
    year = db.Column('year', db.Integer)
    tg_user_id = db.Column('tg_user_id', db.BigInteger)
    application = relationship("Application", backref='users')
    viloyat_id = db.Column(db.Integer, db.ForeignKey('viloyat.id'))
    def init(self, fio, phone, tg_user_id):
        self.fio = fio
        self.phone = phone
        self.tg_user_id = tg_user_id

    def repr(self):
        return f"{self.id}"

class Viloyat(BaseModel, db.Model):
    tablename = 'viloyat'
    name_uz = db.Column('name_uz', db.String(150))
    name_ru = db.Column('name_ru', db.String(150))
    name_uz_kir = db.Column('name_uz_kir', db.String(150))
    user = relationship("User", backref='viloyati')
    tumans = relationship("Tuman", backref='viloyati_tuman')
    users = relationship("User", backref='users_viloyat')

class Tuman(BaseModel, db.Model):
    tablename = 'tuman'
    name_uz2 = db.Column('name_uz2', db.String(150))
    name_ru2 = db.Column('name_ru2', db.String(150))
    name_uz_kir2 = db.Column('name_uz_kir2', db.String(150))
    viloyat_id = db.Column(db.Integer, db.ForeignKey('viloyat.id'))
    mahalas = relationship("Mfy", backref='mahala')
    users = relationship("User", backref='users_tuman')


class Mfy(BaseModel, db.Model):
    tablename = 'mfy'
    name_uz = db.Column('name_uz', db.String(150))
    name_ru = db.Column('name_ru', db.String(150))
    name_uz_kir = db.Column('name_uz_kir', db.String(150))
    tuman_id = db.Column(db.Integer, db.ForeignKey('tuman.id'))
    users = relationship("User", backref='users_mfy')

class AdminUser(BaseModel, db.Model):
    __tablename__ = 'admin'
    login = db.Column(db.String, unique = True)
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    password = db.Column(db.String)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    
    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password=password)


    def check_password(self,password):
        return check_password_hash(self.password, password)

class Category(BaseModel, db.Model):
    __tablename__ = 'category'
    name_uz = db.Column(db.String)
    name_uz_kir = db.Column(db.String)
    name_ru = db.Column(db.String)

    admins = relationship("AdminUser", backref = 'category')

    def init(self, name):
        self.name = name


class Application(BaseModel, db.Model):
    __tablename__ = 'application'
    status = db.Column(db.String, default='pending')
    application = db.Column(db.Text)
    answer = db.Column(db.String)
    lang = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def int(self, status, application, answer, user_id, category_id):
        self.status = status
        self.application = application
        self.answer = answer
        self.user_id = user_id
        self.category_id = category_id
    
    def format(self):
        name, phone = db.session.query(User.fio, User.phone).filter(User.id == self.user_id).first()
        return {
            'id' : self.id,
            'application' : self.application,
            'answer' : self.answer,
            'user_fio' : name,
            'user_phone' : phone 
        }

class Text(BaseModel, db.Model):
    __tablename__ = 'text'
    greeting = db.Column('greeting', db.Text)
    step1 = db.Column('step1', db.String)
    step2 = db.Column('step2', db.String)
    step3 = db.Column('step3', db.Text)
    step4 = db.Column('step4', db.Text)
    lang = db.Column('lang', db.Text)

    def int(self, id, greeting, step1, step2, step3, step4, lang):
        self.id = id
        self.greeting = greeting
        self.step1 = step1
        self.step2 = step2
        self.step3 = step3
        self.step4 = step4
        self.lang = lang
     


    