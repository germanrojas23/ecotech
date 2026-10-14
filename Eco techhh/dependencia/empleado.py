class Empleado:

    def __init__(
        self,
        id_empleado,
        nombre,
        direccion,
        telefono,
        correo,
        salario,
        fecha_inicio
    ):
        if not isinstance(id_empleado, int) or isinstance(id_empleado, bool) or id_empleado <= 0:
            raise ValueError("El ID debe ser un entero positivo.")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")

        if not isinstance(direccion, str) or not direccion.strip():
            raise ValueError("La direccion no puede estar vacia.")

        if not isinstance(telefono, str) or not telefono.strip():
            raise ValueError("El telefono no puede estar vacio.")

        if not isinstance(correo, str) or "@" not in correo:
            raise ValueError("El correo no es valido.")

        if isinstance(salario, bool) or not isinstance(salario, (int, float)) or not 0 <= salario <= 100000000:
            raise ValueError("El salario debe estar entre 0 y 100.000.000.")

        if not isinstance(fecha_inicio, str) or not fecha_inicio.strip():
            raise ValueError("La fecha de inicio no puede estar vacia.")

        self.__id_empleado = id_empleado
        self.__nombre = nombre.strip()
        self.__direccion = direccion.strip()
        self.__telefono = telefono.strip()
        self.__correo = correo.strip()
        self.__salario = salario
        self.__fecha_inicio = fecha_inicio.strip()

    def obtener_datos(self):
        return {
            "id": self.__id_empleado,
            "nombre": self.__nombre,
            "direccion": self.__direccion,
            "telefono": self.__telefono,
            "correo": self.__correo,
            "salario": self.__salario,
            "fechaInicio": self.__fecha_inicio
        }

    def editar(self, nombre, direccion, telefono, correo, salario, fecha_inicio):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")

        if not direccion.strip():
            raise ValueError("La direccion no puede estar vacia.")

        if not telefono.strip():
            raise ValueError("El telefono no puede estar vacio.")

        if "@" not in correo:
            raise ValueError("El correo no es valido.")

        if isinstance(salario, bool) or not isinstance(salario, (int, float)) or not 0 <= salario <= 100000000:
            raise ValueError("El salario no es valido.")

        if not fecha_inicio.strip():
            raise ValueError("La fecha de inicio no puede estar vacia.")

        self.__nombre = nombre.strip()
        self.__direccion = direccion.strip()
        self.__telefono = telefono.strip()
        self.__correo = correo.strip()
        self.__salario = salario
        self.__fecha_inicio = fecha_inicio.strip()
