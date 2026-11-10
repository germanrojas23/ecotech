"""Almacena de forma local el historial de consultas externas."""
import json
from conexion import conectar
from dependencia.seguridad import exigir_sesion

class ConsultaDAO:
    def crear_tabla(self):
        with conectar() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS consultas_api (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
                tipo TEXT NOT NULL, datos_json TEXT NOT NULL,
                consultado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")

    def guardar(self, usuario, tipo, datos):
        exigir_sesion(usuario)
        if tipo not in {"clima", "tipo_cambio"} or not isinstance(datos, dict):
            raise ValueError("Los datos de consulta no tienen un formato válido.")
        contenido = json.dumps(datos, ensure_ascii=False, allow_nan=False)
        with conectar() as db:
            db.execute("INSERT INTO consultas_api(usuario_id,tipo,datos_json) VALUES(?,?,?)",
                       (usuario["id"], tipo, contenido))

    def listar_usuario(self, usuario):
        exigir_sesion(usuario)
        with conectar() as db:
            return db.execute("SELECT tipo,datos_json,consultado_en FROM consultas_api WHERE usuario_id=? ORDER BY id DESC LIMIT 50",
                              (usuario["id"],)).fetchall()
