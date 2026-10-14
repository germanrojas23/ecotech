class ControlAcceso:

    def __init__(self):
        self.__usuarios = []

    def registrar_usuario(self, usuario):
        self.__usuarios.append(usuario)

    def autenticar_usuario(self, correo, contrasena):
        for usuario in self.__usuarios:
            datos = usuario.obtener_datos()

            if datos["correo"] == correo:
                if usuario.verificar_contrasena(contrasena):
                    return usuario

        return None