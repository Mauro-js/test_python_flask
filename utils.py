from itsdangerous import URLSafeTimedSerializer

from main import app

def get_token(base):
    return URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(base, salt=app.config['SECURITY_PASSWORD_SALT'])


def check_token(token):
    return URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt=app.config['SECURITY_PASSWORD_SALT'])
