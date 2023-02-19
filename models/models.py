from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from main import db

class Votante(db.Model):
    __tablename__ = 'votantes'

    id = db.Column(db.Integer, primary_key=True, default=db.text("nextval('votantes_id_seq')"))
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
    ya_voto = db.Column(db.Boolean, default=False, nullable=False)
    nro_socio = db.Column(db.Integer, unique=True)

class Sufragio(db.Model):
    __tablename__ = 'sufragio'

    id = db.Column(db.Integer, primary_key=True, default=db.text("nextval('sufragio_id_seq')"))
    lista = db.Column(db.Integer)
    anulado = db.Column(db.Boolean, default=False, nullable=False)
    blanco = db.Column(db.Boolean, default=False, nullable=False)


class Resultado(db.Model):
    __tablename__ = 'resultado'

    id = db.Column(db.Integer, primary_key=True, default=db.text("nextval('resultado_id_seq')"))
    cantidad_habilitados = db.Column(db.Integer)
    cantidad_votantes = db.Column(db.Integer)

    def incrementar_cantidad_habilitados(self):
        self.cantidad_habilitados += 1
        db.session.commit()

    def incrementar_cantidad_votantes(self):
        self.cantidad_votantes += 1
        db.session.commit()

    def get_first_resultado():
        return Resultado.query.first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Padron(db.Model):
    __tablename__ = 'padron'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=db.text("nextval('padron_id_seq')"))
    nro_socio = db.Column(db.Integer)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_nro(nro_socio):
        return Padron.query.filter_by(nro_socio=nro_socio).first()


class Lista(db.Model):
    __tablename__ = 'lista'

    id = db.Column(db.Integer, primary_key=True, default=db.text("nextval('list_id_seq')"))
    nombre = db.Column(db.String, nullable=False)
    cantidad_votos = db.Column(db.Integer)
    presidente = db.Column(db.String, nullable=False)
    vicepresidente = db.Column(db.String, nullable=False)

    @staticmethod
    def get_by_name(nombre):
        return Lista.query.filter_by(nombre=nombre).first()

    def incrementar_votos(self):
        self.cantidad_votos += 1
        db.session.commit()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class Users(db.Model, UserMixin):
    ___tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, default=db.text("nextval('users_id_seq')"))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email_confirmed_at = db.Column(db.DateTime())
    voto = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    nro_socio = db.Column(db.Integer)

    def __repr__(self):
        return '<User {} - Email {}>'.format(self.name, self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Users.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email=email).first()

