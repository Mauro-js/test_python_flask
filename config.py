import os
from jinja2 import Environment, FileSystemLoader

# Configurar el directorio de plantillas
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

# Crear un ambiente de Jinja2
jinja_env = Environment(loader=FileSystemLoader(template_dir))

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD

POSTGRES = {
    'user': 'myuser',
    'pw': 'mypassword',
    'db': 'mydb',
    'host': 'localhost',
    'port': '5432',
}


SECRET_KEY =  'A SECRET KEY'

SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = f"postgres://{POSTGRES['user']}:" \
                          f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                          f"{POSTGRES['port']}/{POSTGRES['db']}"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = 'niev.mauro@gmail.com'
MAIL_PASSWORD = 'roagcvjtmnohlziy'


MAIL_DEFAULT_SENDER = 'niev.mauro@gmail.com'