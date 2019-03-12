from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash

from ..models.user import User
from ..db import get_db
from .errors import forbidden, unauthorized
from . import api


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    database = get_db()
    doc = database.collection(u"users").where(u"email", u"==", email_or_token)
    try:
        user = [User.from_dict(i.to_dict()) for i in doc.get()][0]
        g.current_user = user
        g.token_used = False
        return user.verify_password(password)
    except:
        return False


@api.before_request
@auth.login_required
def before_request():
    if g.current_user is None and request.endpoint != "search":
        return forbidden('Unconfirmed account')


@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})