from main import db, app
from models.models import Votante, Sufragio, Padron, Resultado, Lista, Users
import re

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData

with app.app_context():
    db.drop_all()
    db.create_all()

    POSTGRES = {
        'user': 'myuser',
        'pw': 'mypassword',
        'db': 'mydb',
        'host': 'localhost',
        'port': '5432',
    }

    SQLALCHEMY_DATABASE_URI = f"postgres://{POSTGRES['user']}:" \
                              f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                              f"{POSTGRES['port']}/{POSTGRES['db']}"

    # Crear conexión a la base de datos
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    # Obtener metadata
    metadata = MetaData()

    # Definir las secuencias
    sequences = [
        'votantes_id_seq',
        'sufragio_id_seq',
        'resultado_id_seq',
        'padron_id_seq',
        'list_id_seq',
        'users_id_seq'
    ]

    for seq in sequences:
        try:
            # Verificar si la secuencia existe
            engine.execute("SELECT nextval('{}')".format(seq))
        except:
            # Crear secuencia en caso de no existir
            engine.execute("CREATE SEQUENCE {}".format(seq))

    archivo = open("padron.html", "r",  encoding="utf8")
    padron = archivo.read()
    pattern = re.compile("</span>(\d\d\d)</div>")
    matching = pattern.findall(padron)
    print(matching)
    for n in matching:
        padron = Padron(nro_socio=n)
        padron.save()

    u1 = Users(name='admin', email='admin@antel.com.uy', is_admin=True, email_confirmed_at=datetime.now())
    u1.set_password("admin123")
    u1.save()

    resultado = Resultado(cantidad_habilitados=0, cantidad_votantes=0)
    resultado.save()

    users = Users.query.all()
    print(users)

    admin = Users.get_by_email('admin@antel.com.uy')
    print(admin)

    get_resultado = Resultado.query.all()
    print(get_resultado)

    # Agregar la siguiente línea para contar las filas en la tabla Padron
    print("Cantidad de registros en la tabla Padron: ", Padron.query.count())
    print("Cantidad de registros en la tabla Users: ", Users.query.count())
