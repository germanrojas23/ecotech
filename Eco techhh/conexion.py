import sqlite3


def conectar():
    try:
        conexion = sqlite3.connect("ecotech_uml.db")
        return conexion

    except sqlite3.Error as error:
        print("Error al conectar con la base de datos:", error)
        return None