class RegistroTiempo:

    def __init__(self, id_registro, fecha, horas, descripcion):
        if not isinstance(id_registro, int) or isinstance(id_registro, bool) or id_registro <= 0:
            raise ValueError("El ID debe ser un entero positivo.")

        if not fecha.strip():
            raise ValueError("La fecha no puede estar vacia.")

        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas deben ser un numero positivo.")

        if not descripcion.strip():
            raise ValueError("La descripcion no puede estar vacia.")

        self.__id = id_registro
        self.__fecha = fecha.strip()
        self.__horas = horas
        self.__descripcion = descripcion.strip()

    def registrar_horas(self, nuevas_horas):
        if isinstance(nuevas_horas, bool) or not isinstance(nuevas_horas, (int, float)) or nuevas_horas <= 0:
            raise ValueError("Las horas deben ser un numero positivo.")

        self.__horas = nuevas_horas

    def validar_datos(self):
        return (
            self.__id > 0
            and bool(self.__fecha)
            and self.__horas > 0
            and bool(self.__descripcion)
        )

    def exportar_informe(self):
        return {
            "id": self.__id,
            "fecha": self.__fecha,
            "horas": self.__horas,
            "descripcion": self.__descripcion
        }

    def obtener_datos(self):
        return self.exportar_informe()