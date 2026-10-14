from dependencia.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO


def solicitar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))

            if valor <= 0:
                print("El valor debe ser un entero positivo.")
                continue

            return valor

        except ValueError:
            print("Error: ingresa un numero entero valido.")


def solicitar_texto(mensaje):
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("Error: este campo no puede estar vacio.")


def solicitar_correo():
    while True:
        correo = solicitar_texto("Correo: ")

        if "@" in correo and "." in correo.split("@")[-1]:
            return correo

        print("Error: ingresa un correo valido.")


def solicitar_salario():
    while True:
        try:
            salario = float(input("Salario: "))

            if not 0 <= salario <= 100000000:
                print("El salario debe estar entre 0 y 100.000.000.")
                continue

            return salario

        except ValueError:
            print("Error: ingresa un salario numerico valido.")


def solicitar_datos_empleado():
    nombre = solicitar_texto("Nombre: ")
    direccion = solicitar_texto("Direccion: ")
    telefono = solicitar_texto("Telefono: ")
    correo = solicitar_correo()
    salario = solicitar_salario()
    fecha_inicio = solicitar_texto("Fecha de inicio (DD/MM/AAAA): ")

    return nombre, direccion, telefono, correo, salario, fecha_inicio


def registrar_empleado(dao):
    print("\n=== REGISTRAR EMPLEADO ===")

    id_empleado = solicitar_entero("ID: ")
    datos = solicitar_datos_empleado()

    try:
        empleado = Empleado(id_empleado, *datos)

        if dao.registrar(empleado):
            print("Empleado registrado correctamente.")
        else:
            print("No se pudo registrar. Comprueba que el ID no exista.")

    except ValueError as error:
        print("Error de validacion:", error)


def consultar_empleados(dao):
    empleados = dao.listar()

    if not empleados:
        print("\nNo hay empleados registrados.")
        return

    print("\n=== LISTA DE EMPLEADOS ===")

    for empleado in empleados:
        print(
            f"\nID: {empleado[0]}"
            f"\nNombre: {empleado[1]}"
            f"\nDireccion: {empleado[2]}"
            f"\nTelefono: {empleado[3]}"
            f"\nCorreo: {empleado[4]}"
            f"\nSalario: ${empleado[5]:,.0f}"
            f"\nFecha de inicio: {empleado[6]}"
        )


def actualizar_empleado(dao):
    print("\n=== ACTUALIZAR EMPLEADO ===")

    id_empleado = solicitar_entero("ID del empleado: ")
    datos = solicitar_datos_empleado()

    try:
        # Validar los datos antes de actualizar la base de datos.
        Empleado(id_empleado, *datos)

        if dao.actualizar(id_empleado, *datos):
            print("Empleado actualizado correctamente.")
        else:
            print("No se encontro el empleado indicado.")

    except ValueError as error:
        print("Error de validacion:", error)


def eliminar_empleado(dao):
    print("\n=== ELIMINAR EMPLEADO ===")

    id_empleado = solicitar_entero("ID del empleado: ")

    confirmar = input(
        "¿Estas seguro de eliminarlo? (s/n): "
    ).strip().lower()

    if confirmar == "s":
        if dao.eliminar(id_empleado):
            print("Empleado eliminado correctamente.")
        else:
            print("No se encontro el empleado indicado.")
    else:
        print("Operacion cancelada.")


def main():
    dao = EmpleadoDAO()

    if not dao.crear_tabla():
        print("No se pudo preparar la base de datos.")
        return

    while True:
        print("\n===== ECOTECH SOLUTIONS =====")
        print("1. Registrar empleado")
        print("2. Consultar empleados")
        print("3. Actualizar empleado")
        print("4. Eliminar empleado")
        print("5. Salir")

        opcion = input("Selecciona una opcion: ").strip()

        try:
            if opcion == "1":
                registrar_empleado(dao)

            elif opcion == "2":
                consultar_empleados(dao)

            elif opcion == "3":
                actualizar_empleado(dao)

            elif opcion == "4":
                eliminar_empleado(dao)

            elif opcion == "5":
                print("Saliendo del sistema.")
                break

            else:
                print("Opcion no valida. Selecciona del 1 al 5.")

        except Exception as error:
            print("Ocurrio un error inesperado:", error)


if __name__ == "__main__":
    main()