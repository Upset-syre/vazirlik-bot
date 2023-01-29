from flask import *
import requests
from json import loads
from app.core import token_required
from telebot import types,TeleBot
from flask_login import login_required, login_user, current_user
from app.models import *



home = Blueprint("home", __name__, url_prefix='/home')


@home.route('/create/admin', methods = ['POST', 'GET'])
def create_admin():
    login = 'admin'
    password = '12345678'
    adm = AdminUser(
        login = login,
        name = "Master",
    )
    adm.set_password(password=password)
    db.session.add(adm)
    db.session.commit()
    return jsonify({
        'msg':'ok'
    })


@home.route("/login",methods = ['POST','GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        
        adm = AdminUser.query.filter_by(login=form.login.data).first()

        if adm:
            if adm.check_password(form.password.data):
                adm.is_authenticated = True
                
                print("hi")

                db.session.commit()
                login_user(adm)
                print(url_for('home.home_page'))
                return redirect(url_for('home.home_page'))
    

    return render_template('signin.html',form = form)

    

@home.route("/",methods = ['GET', 'POST'])
@login_required
def home_page():
    pending = 0
    progress = 0
    completed = 0
    all_users = 0
    if current_user.category_id:
        pending = len(db.session.query(Application.id).filter_by(status = 'pending', category_id = current_user.category_id).all())

        completed = len(db.session.query(Application.id).filter_by(status = 'completed',category_id = current_user.category_id).all())

        progress = len(db.session.query(Application.id).filter_by(status = 'progress', category_id = current_user.category_id).all())

        all_users = len(db.session.query(User.id).all())
    else:
        pending = len(db.session.query(Application.id).filter_by(status = 'pending').all())
        completed = len(db.session.query(Application.id).filter_by(status = 'completed').all())
        progress = len(db.session.query(Application.id).filter_by(status = 'progress').all())
        all_users = len(db.session.query(User.id).all())
    
    return render_template('dashboard.html', pending = pending, progress = progress, completed = completed, all_users = all_users, active = 1)



@home.route("/pending",methods = ['GET', 'POST'])
@login_required
def pending_page():
    pending = 0
    progress = 0
    completed = 0
    all_categories = 0

    if current_user.category_id:
        all_categories = db.session.query(Category.id, Category.name).filter(Category.id == current_user.category_id).first()
        
        pending = [x.format() for x in db.session.query(Application.id).filter_by(status = 'pending', category_id = current_user.category_id).all()]

        completed = len(db.session.query(Application.id).filter_by(status = 'completed',category_id = current_user.category_id).all())

        progress = len(db.session.query(Application.id).filter_by(status = 'progress', category_id = current_user.category_id).all())

        all_users = len(db.session.query(User.id).all())
    else:
        all_categories = db.session.query(Category.id, Category.name).all()

        pending = len(db.session.query(Application.id).filter_by(status = 'pending').all())
        completed = len(db.session.query(Application.id).filter_by(status = 'completed').all())
        progress = len(db.session.query(Application.id).filter_by(status = 'progress').all())
        all_users = len(db.session.query(User.id).all())
    
    return render_template('pending.html', pending = pending, progress = progress, completed = completed, all_users = all_users,all_categories = all_categories , active = 2)