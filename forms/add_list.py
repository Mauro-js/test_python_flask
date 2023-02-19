from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

class ListaForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    presidente = StringField('Presidente',  validators=[DataRequired()])
    vicepresidente = StringField('Vicepresidente', validators=[DataRequired()])
    nro_socio = StringField('Numero de Socio')
    submit = SubmitField('Agregar')
