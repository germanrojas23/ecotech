class Proyecto:

    def __init__(
        self,
        id_proyecto,
        nombre,
        descripcion,
        fecha_inicio
    ):
        self.__id_proyecto = id_proyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
        self.__empleados = []

    def crear(self):
        return True

    def editar(self, nombre, descripcion, fecha_inicio):
        if not nombre.strip():
            return False

        if not descripcion.strip():
            return False

        if not fecha_inicio.strip():
            return False

        self.__nombre = nombre.strip()
        self.__descripcion = descripcion.strip()
        self.__fecha_inicio = fecha_inicio.strip()
        return True

    def eliminar(self):
        self.__empleados.clear()
        return True

    def asignar_empleado(self, empleado):
        self.__empleados.append(empleado)

    def obtener_datos(self):
        return {
            "id": self.__id_proyecto,
            "nombre": self.__nombre,
            "descripcion": self.__descripcion,
            "fechaInicio": self.__fecha_inicio,
            "cantidad_empleados": len(self.__empleados)
        }