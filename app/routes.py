from flask import *
import requests
from json import loads
from app.core import token_required
from flask_login import login_required, login_user, current_user, logout_user

from app.models import *

Per_page = 15

home = Blueprint("home", __name__, url_prefix='/home')

# token='5979258364:AAGdicjuOiyXTMoZj1Z44FMUeu84bcbnAzw'
token='6272081757:AAH-YmPy-AKD5Ang_tJoPXN8p3nkocjr8Ls'

@home.route('/create/admin', methods = ['POST', 'GET'])
def create_admin():
    if request.method == 'GET':
        admins = [{
            'login' : x.login,
            'password' : '12345678',
            'category_name' : db.session.query(Category.name_uz).filter(Category.id == x.category_id).first()[0] if x.category_id else None
        } for x in AdminUser.query.all()]
        return jsonify(admins)

    login = 'user'
    password = '12345678'
    for x in range(10):
        adm = AdminUser(
            login = login + str(x+1),
            name = "Subadmin",
            category_id = x+1
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



@home.route("/pending/<int:page>",methods = ['GET', 'POST'])
@login_required
def pending_page( page):
    pending = 0
    pending = db.session.query(Application).filter_by(status = 'pending').order_by(Application.id.desc()).paginate(page = page, per_page = Per_page)
        
        
    
    return render_template('pending.html', pending = pending , active = 2, page = page)




@home.route("/completed/<int:category_id>/<int:page>",methods = ['GET', 'POST'])
@login_required
def completed_page(category_id, page):
    completed = 0
    all_categories = 0
    # if current_user.category_id:
    #     all_categories = db.session.query(Category.id, Category.name_uz).filter(Category.id == current_user.category_id).all()
        
    #     completed = db.session.query(Application).filter_by(status = 'completed', category_id = current_user.category_id).paginate(page = page, per_page = Per_page)

    # else:
    if category_id != 0:
        completed = db.session.query(Application).filter_by(status = 'completed', category_id = category_id).paginate(page = page, per_page = Per_page)
    else:
        completed = db.session.query(Application).filter_by(status = 'completed').paginate(page = page, per_page = Per_page)
    
    # all_categories = db.session.query(Category.id, Category.name_uz).all()
        
    
    return render_template('completed.html', completed = completed, active = 4, category_id = category_id, page = page)


@home.route("/progress/<int:page>",methods = ['GET', 'POST'])
@login_required
def progress_page(page):
    progress = 0
    progress = db.session.query(Application).filter_by(status = 'progress').order_by(Application.id).paginate(page = page, per_page = Per_page)
    print()
    return render_template('progress.html', progress = progress, active = 3, page = page)


@home.route('/all_users/<int:page>', methods = ['POST','GET'])
def all_users_page(page):
    all_users = db.session.query(User).paginate(page = page, per_page = Per_page)
    return render_template('all_users.html', all_users = all_users, page = 1, active = 5)





@home.route('/send/<int:application_id>', methods = ['POST', 'GET'])
def send_answer(application_id):
    form = SendAnswerForm()
    
    if form.validate_on_submit():
        applic = db.session.query(Application).filter_by(id = application_id).first()
        if applic:
            applic.answer = form.answer.data
            applic.status = 'completed'
            db.session.commit()
            if applic.users.lang == 'uz':
                msg = "Hurmatli foydalanuvchi, sizning №" + str(applic.id) + " sonli murojatingiz ko'rib chiqildi!" + '\nJavob: ' + str(applic.answer)
            elif applic.users.lang == 'ru':
                msg = "Уважаемый пользователь, отправленное вами обращение под №" + str(applic.id) + " было рассмотрено!" + '\nОтвет: ' + str(applic.answer)
            else:
                msg = "Húrmetli paydalanɪwshɪ sizdiń  №" + str(applic.id) + " sanlɪ múrájatińiz ko'rip shɪg'ɪldɪ !" + '\nJuwap: ' + str(applic.answer)
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": applic.users.tg_user_id, "text": msg}

            requests.post(url, data=data)
            

            # return redirect(url_for("home.progress_page",category_id = 0, page = 1 ))
            return redirect(url_for("home.pending_page",category_id = 0, page = 1 ))
            

    query = db.session.query(Application).filter_by(id = application_id).first()
    return render_template("send_answer.html", application = query, form = form)



@home.route('/setprogress/<int:application_id>', methods = ['GET'])
def set_progress(application_id):
    appl = Application.query.get_or_404(application_id)
    appl.status = 'progress'
    
    if appl.users.lang == 'uz':
        msg = "Hurmatli foydalanuvchi, sizning №" + str(appl.id) + " sonli murojatingiz ko'rib chiqilmoqda!"
    elif appl.users.lang == 'ru':
        msg = "Уважаемый пользователь, отправленное вами обращение под №" + str(appl.id) + " находится на рассмотрении!"
    else:
        msg = "Húrmetli paydalanɪwshɪ sizdiń  №" + str(appl.id) + " sanlɪ múrájatińiz ko'rip shɪg'ɪlmaqta !"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": appl.users.tg_user_id, "text": msg}
    requests.post(url, data=data)

    db.session.commit()
    return redirect(url_for('home.pending_page', category_id = 0, page = 1))


@home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))



@home.route('/search')
def search():
    keyword = request.args.get('s')
    progress = 0
    progress = Application.query.msearch(keyword, fields=['application', 'answer'] )
    print()
    return render_template('send_answer.html', progress = progress)