import psycopg2

def check_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mydb",
            user="myuser",
            password="mypassword"
        )
        print("Conexión a la base de datos exitosa")
    except psycopg2.Error as e:
        print("Error al conectarse a la base de datos: ", e)
    finally:
        if connection:
            connection.close()
            print("Conexión cerrada.")

check_db_connection()