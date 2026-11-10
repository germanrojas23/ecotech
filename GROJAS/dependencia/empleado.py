"""Entidad Empleado con validaciones de dominio."""
from datetime import datetime
from dependencia.seguridad import validar_texto, validar_correo

class Empleado:
    def __init__(self, id_empleado, nombre, direccion, telefono, correo, salario, fecha_inicio):
        if not isinstance(id_empleado, int) or isinstance(id_empleado, bool) or id_empleado <= 0:
            raise ValueError("El ID debe ser un entero positivo.")
        nombre = validar_texto(nombre, "El nombre", 100)
        direccion = validar_texto(direccion, "La dirección", 160)
        telefono = validar_texto(telefono, "El teléfono", 25)
        correo = validar_correo(correo)
        if isinstance(salario, bool) or not isinstance(salario, (int, float)) or not 0 <= salario <= 100_000_000:
            raise ValueError("El salario debe estar entre 0 y 100.000.000.")
        fecha_inicio = validar_texto(fecha_inicio, "La fecha", 10)
        try:
            datetime.strptime(fecha_inicio, "%d/%m/%Y")
        except ValueError:
            raise ValueError("La fecha debe tener formato DD/MM/AAAA y ser válida.") from None
        self.__id_empleado, self.__nombre = id_empleado, nombre
        self.__direccion, self.__telefono = direccion, telefono
        self.__correo, self.__salario, self.__fecha_inicio = correo, float(salario), fecha_inicio

    def obtener_datos(self):
        return {"id": self.__id_empleado, "nombre": self.__nombre, "direccion": self.__direccion,
                "telefono": self.__telefono, "correo": self.__correo, "salario": self.__salario,
                "fechaInicio": self.__fecha_inicio}

    def editar(self, nombre, direccion, telefono, correo, salario, fecha_inicio):
        actualizado = Empleado(self.__id_empleado, nombre, direccion, telefono, correo, salario, fecha_inicio)
        datos = actualizado.obtener_datos()
        self.__nombre, self.__direccion, self.__telefono = datos["nombre"], datos["direccion"], datos["telefono"]
        self.__correo, self.__salario, self.__fecha_inicio = datos["correo"], datos["salario"], datos["fechaInicio"]
