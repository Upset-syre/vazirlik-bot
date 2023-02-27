from flask import *
import requests
from json import loads
from app.core import token_required
from flask_login import login_required, login_user, current_user

from app.models import *

Per_page = 15

home = Blueprint("home", __name__, url_prefix='/home')

token='5979258364:AAGdicjuOiyXTMoZj1Z44FMUeu84bcbnAzw'


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



@home.route("/pending/<int:category_id>/<int:page>",methods = ['GET', 'POST'])
@login_required
def pending_page(category_id, page):
    pending = 0
    all_categories = 0
    if current_user.category_id:
        all_categories = db.session.query(Category.id, Category.name_uz).filter(Category.id == current_user.category_id).all()
        
        pending = db.session.query(Application).filter_by(status = 'pending', category_id = current_user.category_id).paginate(page = page, per_page = Per_page)

    else:
        if category_id != 0:
            pending = db.session.query(Application).filter_by(status = 'pending', category_id = category_id).paginate(page = page, per_page = Per_page)
        else:
            pending = db.session.query(Application).filter_by(status = 'pending').paginate(page = page, per_page = Per_page)
        
        all_categories = db.session.query(Category.id, Category.name_uz).all()
        
    
    return render_template('pending.html', pending = pending, all_categories = all_categories , active = 2, category_id = category_id, page = page)



@home.route("/completed/<int:category_id>/<int:page>",methods = ['GET', 'POST'])
@login_required
def completed_page(category_id, page):
    completed = 0
    all_categories = 0
    if current_user.category_id:
        all_categories = db.session.query(Category.id, Category.name_uz).filter(Category.id == current_user.category_id).all()
        
        completed = db.session.query(Application).filter_by(status = 'completed', category_id = current_user.category_id).paginate(page = page, per_page = Per_page)

    else:
        if category_id != 0:
            completed = db.session.query(Application).filter_by(status = 'completed', category_id = category_id).paginate(page = page, per_page = Per_page)
        else:
            completed = db.session.query(Application).filter_by(status = 'completed').paginate(page = page, per_page = Per_page)
        
        all_categories = db.session.query(Category.id, Category.name_uz).all()
        
    
    return render_template('completed.html', completed = completed, all_categories = all_categories , active = 4, category_id = category_id, page = page)


@home.route("/progress/<int:category_id>/<int:page>",methods = ['GET', 'POST'])
@login_required
def progress_page(category_id, page):
    progress = 0
    all_categories = 0
    if current_user.category_id:
        all_categories = db.session.query(Category.id, Category.name_uz).filter(Category.id == current_user.category_id).all()
        
        progress = db.session.query(Application).filter_by(status = 'progress', category_id = current_user.category_id).paginate(page = page, per_page = Per_page)

    else:
        if category_id != 0:
            progress = db.session.query(Application).filter_by(status = 'progress', category_id = category_id).paginate(page = page, per_page = Per_page)
        else:
            progress = db.session.query(Application).filter_by(status = 'progress').paginate(page = page, per_page = Per_page)
        
        all_categories = db.session.query(Category.id, Category.name_uz).all()
        
    
    return render_template('progress.html', progress = progress, all_categories = all_categories , active = 3, category_id = category_id, page = page)


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
            
            msg = "Hurmatli foydalanuvchi sizning №" + str(applic.id) + " sonli murojatingiz ko'rib chiqildi!"

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
    
    msg = "Hurmatli foydalanuvchi sizning №" + str(appl.id) + " sonli murojatingiz ko'rib chiqilmoqda!"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": appl.users.tg_user_id, "text": msg}
    requests.post(url, data=data)

    db.session.commit()
    return redirect(url_for('home.pending_page', category_id = 0, page = 1))


