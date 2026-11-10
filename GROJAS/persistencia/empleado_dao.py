"""Acceso a datos de empleados mediante consultas parametrizadas."""
from conexion import conectar
import sqlite3

class EmpleadoDAO:
    def crear_tabla(self):
        with conectar() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, direccion TEXT NOT NULL,
                telefono TEXT NOT NULL, correo TEXT NOT NULL UNIQUE,
                salario REAL NOT NULL CHECK(salario >= 0), fecha_inicio TEXT NOT NULL)""")
        return True

    def registrar(self, empleado):
        d = empleado.obtener_datos()
        try:
            with conectar() as db:
                db.execute("INSERT INTO empleados VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (d['id'], d['nombre'], d['direccion'], d['telefono'], d['correo'], d['salario'], d['fechaInicio']))
            return True
        except sqlite3.IntegrityError:
            return False

    def listar(self):
        with conectar() as db:
            return db.execute("SELECT id,nombre,direccion,telefono,correo,salario,fecha_inicio FROM empleados ORDER BY id").fetchall()

    def actualizar(self, id_empleado, nombre, direccion, telefono, correo, salario, fecha_inicio):
        try:
            with conectar() as db:
                cur = db.execute("""UPDATE empleados SET nombre=?,direccion=?,telefono=?,correo=?,salario=?,fecha_inicio=? WHERE id=?""",
                    (nombre, direccion, telefono, correo, salario, fecha_inicio, id_empleado))
            return cur.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def eliminar(self, id_empleado):
        with conectar() as db:
            cur = db.execute("DELETE FROM empleados WHERE id=?", (id_empleado,))
        return cur.rowcount > 0
