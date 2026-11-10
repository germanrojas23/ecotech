"""Punto de entrada de EcoTech Solutions - Python 3.10+ / VS Code."""
from getpass import getpass
import sqlite3

from dependencia.empleado import Empleado
from dependencia.seguridad import validar_texto, validar_correo, exigir_administrador
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from persistencia.consulta_dao import ConsultaDAO
from servicios_api import consultar_clima, consultar_tipo_cambio, ErrorServicioAPI


def pedir_texto(mensaje, campo="El dato", maximo=100):
    while True:
        try:
            return validar_texto(input(mensaje), campo, maximo)
        except ValueError as exc:
            print(exc)


def pedir_correo():
    while True:
        try:
            return validar_correo(input("Correo: "))
        except ValueError as exc:
            print(exc)


def pedir_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje).strip())
            if numero > 0:
                return numero
            print("Ingresa un entero positivo.")
        except ValueError:
            print("Ingresa un número entero válido.")


def pedir_datos_empleado():
    nombre = pedir_texto("Nombre: ", "El nombre", 100)
    direccion = pedir_texto("Dirección: ", "La dirección", 160)
    telefono = pedir_texto("Teléfono: ", "El teléfono", 25)
    correo = pedir_correo()
    while True:
        try:
            salario = float(input("Salario: ").strip())
            if 0 <= salario <= 100_000_000:
                break
            print("El salario debe estar entre 0 y 100.000.000.")
        except ValueError:
            print("Ingresa un salario numérico válido.")
    fecha = pedir_texto("Fecha de inicio (DD/MM/AAAA): ", "La fecha", 10)
    return nombre, direccion, telefono, correo, salario, fecha


def preparar_sistema():
    usuarios, consultas, empleados = UsuarioDAO(), ConsultaDAO(), EmpleadoDAO()
    usuarios.crear_tabla()
    consultas.crear_tabla()
    empleados.crear_tabla()
    if usuarios.cantidad() == 0:
        print("\n=== PRIMER INICIO: CREAR ADMINISTRADOR ===")
        while True:
            nombre, correo = pedir_texto("Nombre: ", "El nombre"), pedir_correo()
            clave = getpass("Contraseña (10+ caracteres, incluir letras y números): ")
            confirmar = getpass("Confirmar contraseña: ")
            if clave != confirmar:
                print("Las contraseñas no coinciden.")
                continue
            try:
                usuarios.registrar(nombre, correo, clave, "administrador")
                print("Administrador creado. Ya puedes iniciar sesión.")
                break
            except ValueError as exc:
                print(exc)
    return usuarios, consultas, empleados


def iniciar_sesion(dao):
    print("\n=== INICIO DE SESIÓN ===")
    try:
        correo = pedir_correo()
        clave = getpass("Contraseña: ")
        usuario = dao.autenticar(correo, clave)
        if usuario is None:
            print("Credenciales incorrectas o cuenta inactiva.")
        return usuario
    except (ValueError, sqlite3.Error):
        print("No fue posible validar el acceso. Revisa los datos e intenta nuevamente.")
        return None


def registrar_empleado(dao):
    try:
        empleado = Empleado(pedir_entero("ID: "), *pedir_datos_empleado())
        print("Empleado registrado." if dao.registrar(empleado) else "No se pudo registrar: ID o correo duplicado.")
    except ValueError as exc:
        print(f"Datos inválidos: {exc}")


def listar_empleados(dao):
    filas = dao.listar()
    if not filas:
        print("No hay empleados registrados.")
    for e in filas:
        print(f"ID: {e['id']} | {e['nombre']} | {e['correo']} | ${e['salario']:,.0f} | {e['fecha_inicio']}")


def actualizar_empleado(dao):
    try:
        identificador = pedir_entero("ID del empleado: ")
        datos = pedir_datos_empleado()
        Empleado(identificador, *datos)
        print("Empleado actualizado." if dao.actualizar(identificador, *datos) else "No se encontró o existe un correo duplicado.")
    except ValueError as exc:
        print(f"Datos inválidos: {exc}")


def eliminar_empleado(dao):
    identificador = pedir_entero("ID: ")
    if input("¿Confirmas? (s/n): ").strip().lower() == "s":
        print("Empleado eliminado." if dao.eliminar(identificador) else "No se encontró el empleado.")


def mostrar_datos(datos):
    print("\n--- DATOS RECIBIDOS DESDE LA API ---")
    for clave, valor in datos.items():
        print(f"{clave.replace('_', ' ').capitalize()}: {valor}")


def consultar_servicio(usuario, historial):
    # Doble control: el menú exige sesión y los clientes API también la verifican.
    print("\n1. Dólar observado (USD/CLP)\n2. Clima actual por ciudad")
    opcion = input("Selecciona: ").strip()
    try:
        if opcion == "1":
            resultado, tipo = consultar_tipo_cambio(usuario), "tipo_cambio"
        elif opcion == "2":
            ciudad = pedir_texto("Ciudad: ", "La ciudad", 80)
            resultado, tipo = consultar_clima(ciudad, usuario), "clima"
        else:
            print("Opción no válida.")
            return
        mostrar_datos(resultado)
        try:
            historial.guardar(usuario, tipo, resultado)
            print("Consulta guardada en SQLite.")
        except sqlite3.Error:
            print("Consulta completada, pero no se pudo guardar el historial.")
    except PermissionError as exc:
        print(exc)
    except ValueError as exc:
        print(f"Entrada inválida: {exc}")
    except ErrorServicioAPI as exc:
        print(f"Consulta no disponible: {exc}")


def ver_historial(usuario, historial):
    try:
        filas = historial.listar_usuario(usuario)
        if not filas:
            print("No tienes consultas guardadas.")
        for fila in filas:
            print(f"\n{fila['consultado_en']} | {fila['tipo']} | {fila['datos_json']}")
    except sqlite3.Error:
        print("No fue posible recuperar el historial.")


def administrar_usuarios(usuario, dao):
    try:
        exigir_administrador(usuario)
        for u in dao.listar():
            print(f"ID {u['id']} | {u['nombre']} | {u['correo']} | {u['rol']} | activo={u['activo']}")
        if input("¿Crear cuenta de empleado? (s/n): ").strip().lower() == "s":
            nombre, correo = pedir_texto("Nombre: ", "El nombre"), pedir_correo()
            clave = getpass("Contraseña: ")
            dao.registrar(nombre, correo, clave, "empleado")
            print("Cuenta de empleado creada.")
    except PermissionError as exc:
        print(exc)
    except ValueError as exc:
        print(f"No se pudo crear la cuenta: {exc}")


def menu_usuario(usuario, usuarios, historial, empleados):
    while True:
        print(f"\n=== ECOTECH | {usuario['nombre']} ({usuario['rol']}) ===")
        print("1. Consultar API (clima / dólar)\n2. Ver mi historial")
        if usuario["rol"] == "administrador":
            print("3. Registrar empleado\n4. Listar empleados\n5. Actualizar empleado\n6. Eliminar empleado\n7. Administrar usuarios")
        print("0. Cerrar sesión")
        opcion = input("Opción: ").strip()
        if opcion == "1": consultar_servicio(usuario, historial)
        elif opcion == "2": ver_historial(usuario, historial)
        elif usuario["rol"] == "administrador" and opcion == "3": registrar_empleado(empleados)
        elif usuario["rol"] == "administrador" and opcion == "4": listar_empleados(empleados)
        elif usuario["rol"] == "administrador" and opcion == "5": actualizar_empleado(empleados)
        elif usuario["rol"] == "administrador" and opcion == "6": eliminar_empleado(empleados)
        elif usuario["rol"] == "administrador" and opcion == "7": administrar_usuarios(usuario, usuarios)
        elif opcion == "0":
            print("Sesión cerrada.")
            return
        else: print("Opción no válida o sin permisos.")


def main():
    try:
        usuarios, historial, empleados = preparar_sistema()
        while True:
            print("\n===== ECOTECH SOLUTIONS =====\n1. Iniciar sesión\n0. Salir")
            opcion = input("Opción: ").strip()
            if opcion == "1":
                usuario = iniciar_sesion(usuarios)
                if usuario:
                    menu_usuario(usuario, usuarios, historial, empleados)
            elif opcion == "0":
                print("Hasta pronto.")
                break
            else: print("Opción no válida.")
    except (sqlite3.Error, OSError):
        print("EcoTech no pudo iniciar por un problema de almacenamiento o permisos. Revisa la carpeta del proyecto.")


if __name__ == "__main__":
    main()
