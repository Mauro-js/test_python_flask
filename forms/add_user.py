from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField


class AddUserForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2= PasswordField('Repita su Contraseña', validators=[DataRequired(),EqualTo('password', 'Las contraseñas no coinciden')])
    is_admin = BooleanField('Es administrador')
    email_confirmed_at = DateField('Fecha de confirmación de correo')
    submit = SubmitField('Registro')
