class Departamento:

    def __init__(self, id_departamento, nombre, gerente):
        self.__id_departamento = id_departamento
        self.__nombre = nombre
        self.__gerente = gerente
        self.__empleados = []

    def crear(self):
        return True

    def editar(self, nombre, gerente):
        if not nombre.strip() or not gerente.strip():
            return False

        self.__nombre = nombre.strip()
        self.__gerente = gerente.strip()
        return True

    def asignar_empleado(self, empleado):
        self.__empleados.append(empleado)

    def obtener_datos(self):
        return {
            "id": self.__id_departamento,
            "nombre": self.__nombre,
            "gerente": self.__gerente,
            "cantidad_empleados": len(self.__empleados)
        }
