from app import create_app 
from app.exts import db
from app.models import AdminUser

# username = input('please enter your username   =')
# username2 = input('please enter your prefered username   =')
# pswrd = input('which password do you prefer?   =')
# # 

def admins():
    # if new_user:
    app = create_app()
    u = AdminUser(
            login = 'admin',
            name = 'Dispatcher'
        )
    u.set_password('12345678')
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        db.session.add(u)
        db.session.commit()
    # else:
    #     app = create_app()

    #     with app.app_context():
    #         u = User.query.filter_by(username = username).first()
    #         if u:
    #             try:
    #                 u.username = username2
    #                     # db.drop_all()
    #                     # db.create_all()
    #                 db.session.commit()
                    
    #             except:
    #                 print('username alreday exist')
    #             u.set_password(password)
    #             db.session.commit()
    #         else:
    #             print('fuku')

admins()
