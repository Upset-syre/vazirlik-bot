import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
THREADS_PER_PAGE = 10
CSRF_ENABLED     = True
CSRF_SESSION_KEY = "secret"

#work
# SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@127.0.0.1:5432/vazirlik_bot"

#msi
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/vazirlik_bot"

SECRET_KEY = "secret"
FLASK_ADMIN_SWATCH = "yeti"
FLASK_ADMIN_FLUID_LAYOUT = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_LOGIN_ATTEMPTS = 5
SQLALCHEMY_POOL_SIZE = 1
SQLALCHEMY_MAX_OVERFLOW = 0 