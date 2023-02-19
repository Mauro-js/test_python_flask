from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_mail import Mail


mail = Mail()

# instancia Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'niev.mauro@gmail.com'
app.config['MAIL_PASSWORD'] = 'roagcvjtmnohlziy'


admin = Admin(app)


# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')

# inicializa la base de datos con la config leida
db = SQLAlchemy(app)

# para poder usar Flask-Login
login_manager = LoginManager(app)
login_manager.init_app(app)

# rutas disponibles
from routes import *

# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from models.models import Users, Votante, Sufragio, Padron, Resultado, Lista

# Los modelos que queremos mostrar en el admin
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Votante, db.session))
admin.add_view(ModelView(Sufragio, db.session))
admin.add_view(ModelView(Padron, db.session))
admin.add_view(ModelView(Resultado, db.session))
admin.add_view(ModelView(Lista, db.session))

