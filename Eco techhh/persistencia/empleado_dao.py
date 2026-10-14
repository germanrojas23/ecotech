from conexion import conectar


class EmpleadoDAO:

    def crear_tabla(self):
        conexion = conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    salario REAL NOT NULL,
                    fecha_inicio TEXT NOT NULL
                )
            """)

            conexion.commit()
            return True

        except Exception as error:
            print("Error al crear la tabla:", error)
            return False

        finally:
            conexion.close()

    # CREATE: registrar un empleado
    def registrar(self, empleado):
        conexion = conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()
            datos = empleado.obtener_datos()

            cursor.execute("""
                INSERT INTO empleados (
                    id, nombre, direccion, telefono,
                    correo, salario, fecha_inicio
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datos["id"],
                datos["nombre"],
                datos["direccion"],
                datos["telefono"],
                datos["correo"],
                datos["salario"],
                datos["fechaInicio"]
            ))

            conexion.commit()
            return True

        except Exception as error:
            print("Error al registrar empleado:", error)
            return False

        finally:
            conexion.close()

    # READ: consultar todos los empleados
    def listar(self):
        conexion = conectar()

        if conexion is None:
            return []

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id, nombre, direccion, telefono,
                    correo, salario, fecha_inicio
                FROM empleados
                ORDER BY id
            """)

            return cursor.fetchall()

        except Exception as error:
            print("Error al consultar empleados:", error)
            return []

        finally:
            conexion.close()

    # UPDATE: actualizar un empleado
    def actualizar(
        self,
        id_empleado,
        nombre,
        direccion,
        telefono,
        correo,
        salario,
        fecha_inicio
    ):
        conexion = conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE empleados
                SET nombre = ?,
                    direccion = ?,
                    telefono = ?,
                    correo = ?,
                    salario = ?,
                    fecha_inicio = ?
                WHERE id = ?
            """, (
                nombre,
                direccion,
                telefono,
                correo,
                salario,
                fecha_inicio,
                id_empleado
            ))

            conexion.commit()
            return cursor.rowcount > 0

        except Exception as error:
            print("Error al actualizar empleado:", error)
            return False

        finally:
            conexion.close()

    # DELETE: eliminar un empleado
    def eliminar(self, id_empleado):
        conexion = conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM empleados
                WHERE id = ?
            """, (id_empleado,))

            conexion.commit()
            return cursor.rowcount > 0

        except Exception as error:
            print("Error al eliminar empleado:", error)
            return False

        finally:
            conexion.close()