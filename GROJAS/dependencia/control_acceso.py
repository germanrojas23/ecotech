"""Control de acceso en memoria para apoyar el flujo de autenticación."""
from dependencia.seguridad import verificar_hash

class ControlAcceso:
    def __init__(self):
        self.__usuarios = []

    def registrar_usuario(self, usuario):
        self.__usuarios.append(usuario)

    def autenticar_usuario(self, correo, contrasena):
        for usuario in self.__usuarios:
            datos = usuario.obtener_datos()
            if datos.get("correo") == correo and usuario.iniciar_sesion(contrasena, verificar_hash):
                return usuario
        return None
