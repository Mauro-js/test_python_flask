from main import app, login_manager, mail
from forms.login import LoginForm

from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from models.models import Users, Resultado, Lista, Padron
import datetime
from utils import get_token, check_token
from flask_mail import Message

mail.init_app(app)

def send_email(to, body):
    msg = Message("Confirm Token", sender=app.config["MAIL_DEFAULT_SENDER"], recipients=[to])
    msg.body = body
    mail.send(msg)

@app.route("/")
@login_required
def home():
    resultado_query = Resultado.query.all()[0]
    resultado = {
        'cantidad_habilitados': resultado_query.cantidad_habilitados,
        'cantidad_votantes': resultado_query.cantidad_votantes
    }
    listas = Lista.query.all()
    return render_template('home.html', user=current_user, resultado=resultado, listas=listas)


#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Users.get_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # get by email valida
        user = Users.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):

            if user.email_confirmed_at is None:
                flash('Usuario no confirmado')
                return redirect(url_for('login'))

            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('login')
            return redirect(next_page)

        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('home'))
    # no loggeado, dibujamos el login con el forms vacio
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    # Flask-Principal: Remove session keys
    """
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    identity_changed.send(app, identity=AnonymousIdentity())
    """
    return redirect(url_for('login'))

@app.route('/votar')
@login_required
def votar():

    if current_user.is_admin:
        flash('Los administradores no pueden votar')
        return redirect(url_for('home'))

    if current_user.voto:
        flash('El usuario ya ha votado')
        return redirect(url_for('home'))

    if current_user.nro_socio is None:
        flash('El usuario no esta en el padron')
        return redirect(url_for('home'))

    print(current_user.nro_socio)

    padron_nro = Padron.get_by_nro(current_user.nro_socio)

    if padron_nro is None:
        flash('El usuario no esta en el padron')
        return redirect(url_for('home'))


    all_list = Lista.query.all()

    empty = (len(all_list) == 0)

    return render_template('votar.html', listas=all_list, empty=empty)

@app.route('/confirmar_voto/<name>')
@login_required
def confirmar_voto(name):

    if current_user.is_admin:
        flash('Los administradores no pueden votar')
        return redirect(url_for('home'))

    if current_user.voto:
        flash('El usuario ya ha votado')
        return redirect(url_for('home'))

    if current_user.nro_socio is None:
        flash('El usuario no esta en el padron')
        return redirect(url_for('home'))

    padron_nro = Padron.get_by_nro(current_user.nro_socio)

    if padron_nro is None:
        flash('El usuario no esta en el padron')
        return redirect(url_for('home'))

    lista = Lista.get_by_name(name)
    lista.incrementar_votos()

    resultado = Resultado.get_first_resultado()
    resultado.incrementar_cantidad_votantes()

    current_user.voto = True
    current_user.save()

    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(401)
def unathorized(e):
    return render_template('401.html')

@app.errorhandler(403)
def unathorized(e):
    return render_template('403.html')

from forms.register import RegisterForm

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        nro_socio = form.nro_socio.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Users.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = Users(name=username, email=email, is_admin=False, nro_socio=nro_socio)
            user.set_password(password)
            user.save()

            token = get_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)

            send_email(user.email, html)
            return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route("/confirm_email/<token>", methods=["GET", "POST"])
def confirm_email(token):
    try:
        email = check_token(token)

        user = Users.get_by_email(email=email)

        user.email_confirmed_at = datetime.datetime.now()
        user.save()

        try:
            padron_nro = Padron.get_by_nro(current_user.nro_socio)

            if not padron_nro is None:
                resultado = Resultado.get_first_resultado()
                resultado.incrementar_cantidad_habilitados()
        except:
            flash('El usuario no estará habilitado para votar')

        login_user(user, remember=True)
        return redirect(url_for('home'))
    except Exception as e:
        print("Se produjo un error:", str(e))
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))


@app.route("/sufragio")
def sufragio():
    return render_template('sufragio.html')

@app.route("/resultado")
def resultado():
    return render_template('resultado.html')

@app.route("/ingreso_lista")
def ingreso_lista():
    return render_template('ingreso_lista.html')

from forms.add_user import AddUserForm

@app.route("/add_user")
@login_required
def add_user():
    form = AddUserForm()

    if current_user.is_admin:
        return render_template('add_user.html', form=form)

    return redirect(url_for('home'))

from forms.add_list import ListaForm

@app.route("/add_list", methods=["GET", "POST"])
@login_required
def add_list():
    form = ListaForm()

    if current_user.is_admin:
        error = None
        if form.validate_on_submit():
            name = form.name.data
            presidente = form.presidente.data
            vicepresidente = form.vicepresidente.data
            # Comprobamos que no hay una lista con este nombre
            exist_lista = Lista.get_by_name(name)
            if exist_lista is not None:
                flash('El nombre {} ya está siendo utilizado'.format(name))
            else:
                lista = Lista(nombre=name, cantidad_votos=0, presidente=presidente, vicepresidente=vicepresidente)
                lista.save()

                return redirect(url_for('home'))

        return render_template('add_list.html', form=form)


    return redirect(url_for('home'))

#@auth_bp.route('/confirm/<token>')
#def confirm_email(token):
#    try:
#        email = confirm_token(token)
#    except:
#        flash('The confirmation link is invalid or has expired.', 'danger')
#
#    user = User.query.filter_by(email=email).first_or_404()
#    if user.is_confirmed:
#        flash('Account already confirmed. Please login.', 'success')
#    else:
#        user.is_confirmed = True
#        user.email_confirmed_at = datetime.datetime.now()
#        user.save()
#
#        flash('You have confirmed your account. Thanks!', 'success')
#    return redirect(url_for('home'))