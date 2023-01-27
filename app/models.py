from app import db
from sqlalchemy.orm import relationship
import datetime
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms.validators import InputRequired, Length, ValidationError,DataRequired
from markupsafe import Markup


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()], render_kw = {'placeholder' : 'Login'})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    style={'class': 'loginform', 'style': 'margin-top:12px'}

    submit = SubmitField("Sign in",render_kw = style)



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
    fio = db.Column(db.String)
    phone = db.Column(db.String)
    tg_user_id = db.Column(db.Integer)
    application = relationship("Application", backref='users')

    def init(self, fio, phone, tg_user_id):
        self.fio = fio
        self.phone = phone
        self.tg_user_id = tg_user_id

    def repr(self):
        return f"{self.id}"


class AdminUser(BaseModel, db.Model):
    __tablename__ = 'admin'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    password = db.Column(db.String)



class Category(BaseModel, db.Model):
    __tablename__ = 'category'
    name = db.Column('name', db.String)
    application = relationship("Application", backref='category')
    admins = relationship("AdminUser", backref = 'category')

    def init(self, name):
        self.name = name


class Application(BaseModel, db.Model):
    __tablename__ = 'application'
    status = db.Column('status', db.String, default='pending')
    application = db.Column('application', db.Text, default='pending')
    answer = db.Column('answer', db.String)
    lang = db.Column('lang', db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def int(self, status, application, answer, user_id, category_id):
        self.status = status
        self.application = application
        self.answer = answer
        self.user_id = user_id
        self.category_id = category_id


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
     


    