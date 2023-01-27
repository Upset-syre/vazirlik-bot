from functools import wraps
import jwt, requests
from flask import *
from app.config import SECRET_KEY
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'message' : "Token is missing !!"
            }), 401
        try:
            print(token)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(data)
            current_user = User.query\
                .filter_by(id=data['public_id'])\
                .first()
        except Exception as E:
            return jsonify({
                'message' : str(E)
            }), 401
        return  f(current_user, *args, **kwargs)
  
    return decorated