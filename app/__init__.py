from app.exts import db
from flask import *
from flask_login import LoginManager, current_user, login_user
# from app.adminview.forms import LoginForm
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from app.models import User, Category, Application,Text,AdminUser
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView





login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return AdminUser.query.get(int(id))

def create_app(testing=False):
        # Blueprints
    from app.routes import home

    # from app.smartboard_student.routes import student

    # from app.EDM.routes import edm

    # from app.inet.routes import inet

    # from app.dormitory.routes import dormitory
    # from app.smartboard_teacher.routes import smartboard_teacher
    # from app.tdau.routes import tdau
    # from app.tools.routes import tools


    # from app.tools.routes import tools

    app = Flask(__name__, template_folder = 'templates',static_folder='static',static_url_path='/static')
    if testing:
        app.config.from_pyfile('t_config.py')
    else:
        app.config.from_pyfile('config.py')
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(home)
    # app.register_blueprint(student)
    # app.register_blueprint(edm)
    # app.register_blueprint(tdau)
    # app.register_blueprint(tools)
    # app.register_blueprint(inet)
    # app.register_blueprint(dormitory)
    # app.register_blueprint(smartboard_teacher) 
    
    
    
    # def gg():
        
    #     bot.send_message(201458407, db.session.query(User.name).first())    
    

    @app.route("/", methods=['GET'])
    def home():
        
        # gg()
        return redirect(url_for('home.home_page'))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('home.login'))
    
        

    @app.after_request
    def after_request(response):
        header = response.headers
        header.add('Access-Control-Allow-Origin', '*')
        header.add('Access-Control-Allow-Headers', '*')
        header.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response
    with app.app_context():
        # db.drop_all()
        db.create_all()
        
    admin = Admin(app,name='microblog', template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(, db.session))
    
    
    # @app.route('/adminlogin', methods = ['POST','GET'])
    # def flask_login():
    #     if current_user.is_authenticated:
    #         return redirect(url_for('admin.index'))
    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         user = User.query.filter_by(username=form.login.data).first()
    #         if user is None or not user.check_password(form.password.data):
    #             print('Invalid user or password')
    #             return redirect(url_for('flask_login'))
    #         login_user(user)
    #         return redirect(url_for('admin.index'))
    #     else:
    #         print(form.errors)
    #     return render_template('login.html', form=form)

    # admin.add_view(StudentView(Student, db.session))

    # admin.init_app(app)
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
    return app



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

