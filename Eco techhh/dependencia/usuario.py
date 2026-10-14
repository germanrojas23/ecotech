class Usuario:

    def __init__(self, id_usuario, nombre_usuario, contrasena_hash, rol):

        if not isinstance(id_usuario, int) or isinstance(id_usuario, bool) or id_usuario <= 0:
            raise ValueError("El ID debe ser un entero positivo.")

        if not nombre_usuario.strip():
            raise ValueError("El nombre de usuario no puede estar vacio.")

        if not contrasena_hash.strip():
            raise ValueError("La contrasena no puede estar vacia.")

        if not rol.strip():
            raise ValueError("El rol no puede estar vacio.")

        self.__id = id_usuario
        self.__nombre_usuario = nombre_usuario.strip()
        self.__contrasena_hash = contrasena_hash
        self.__rol = rol.strip()
        self.__sesion_activa = False

    def iniciar_sesion(self, contrasena):
        if contrasena == self.__contrasena_hash:
            self.__sesion_activa = True
            return True

        return False

    def cerrar_sesion(self):
        self.__sesion_activa = False

    def obtener_datos(self):
        return {
            "id": self.__id,
            "nombreUsuario": self.__nombre_usuario,
            "rol": self.__rol,
            "sesionActiva": self.__sesion_activa
        }