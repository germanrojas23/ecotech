"""Persistencia y autenticación de usuarios."""
import sqlite3
from conexion import conectar
from dependencia.seguridad import generar_hash, verificar_hash, validar_correo, validar_texto

class UsuarioDAO:
    def crear_tabla(self):
        with conectar() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('administrador','empleado')),
                activo INTEGER NOT NULL DEFAULT 1, creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")

    def cantidad(self):
        with conectar() as db:
            return db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]

    def registrar(self, nombre, correo, contrasena, rol="empleado"):
        nombre = validar_texto(nombre, "El nombre", 100)
        correo = validar_correo(correo)
        if rol not in {"administrador", "empleado"}:
            raise ValueError("Rol no permitido.")
        password_hash = generar_hash(contrasena)
        try:
            with conectar() as db:
                cur = db.execute("INSERT INTO usuarios(nombre,correo,password_hash,rol) VALUES(?,?,?,?)",
                                 (nombre, correo, password_hash, rol))
                return cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe una cuenta con ese correo.") from None

    def autenticar(self, correo, contrasena):
        correo = validar_correo(correo)
        if not isinstance(contrasena, str) or not contrasena:
            raise ValueError("Debes ingresar tu contraseña.")
        with conectar() as db:
            fila = db.execute("SELECT id,nombre,correo,password_hash,rol FROM usuarios WHERE correo=? AND activo=1", (correo,)).fetchone()
        if fila and verificar_hash(contrasena, fila["password_hash"]):
            return {"id": fila["id"], "nombre": fila["nombre"], "correo": fila["correo"], "rol": fila["rol"]}
        return None

    def listar(self):
        with conectar() as db:
            return db.execute("SELECT id,nombre,correo,rol,activo FROM usuarios ORDER BY id").fetchall()
