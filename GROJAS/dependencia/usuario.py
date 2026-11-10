"""Entidad Usuario: no almacena contraseñas en texto plano."""
class Usuario:
    def __init__(self, id_usuario, nombre_usuario, contrasena_hash, rol):
        if not isinstance(id_usuario, int) or isinstance(id_usuario, bool) or id_usuario <= 0:
            raise ValueError("El ID debe ser un entero positivo.")
        if not isinstance(nombre_usuario, str) or not nombre_usuario.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if not isinstance(contrasena_hash, str) or not contrasena_hash.strip():
            raise ValueError("El hash de contraseña es obligatorio.")
        if rol not in {"administrador", "empleado"}:
            raise ValueError("El rol no es válido.")
        self.__id = id_usuario
        self.__nombre_usuario = nombre_usuario.strip()
        self.__contrasena_hash = contrasena_hash
        self.__rol = rol
        self.__sesion_activa = False

    def iniciar_sesion(self, contrasena, verificador):
        self.__sesion_activa = bool(verificador(contrasena, self.__contrasena_hash))
        return self.__sesion_activa

    def cerrar_sesion(self):
        self.__sesion_activa = False

    def obtener_datos(self):
        return {"id": self.__id, "nombreUsuario": self.__nombre_usuario,
                "rol": self.__rol, "sesionActiva": self.__sesion_activa}
