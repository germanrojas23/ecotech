"""Validación de entradas y almacenamiento seguro de contraseñas.

PBKDF2-HMAC-SHA256 no cifra reversiblemente la contraseña: deriva un hash
con salt aleatorio, apropiado para almacenar credenciales.
"""
import hashlib
import hmac
import re
import secrets

ITERACIONES = 600_000


def validar_texto(valor, campo="El dato", maximo=100):
    if not isinstance(valor, str):
        raise ValueError(f"{campo} debe ser texto.")
    valor = valor.strip()
    if not valor or len(valor) > maximo:
        raise ValueError(f"{campo} es obligatorio y admite hasta {maximo} caracteres.")
    if any(ord(c) < 32 for c in valor):
        raise ValueError(f"{campo} contiene caracteres de control no permitidos.")
    return valor


def validar_correo(correo):
    correo = validar_texto(correo, "El correo", 254).lower()
    patron = r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"
    if not re.fullmatch(patron, correo):
        raise ValueError("Ingresa un correo electrónico válido.")
    return correo


def validar_contrasena(contrasena):
    if not isinstance(contrasena, str) or not 10 <= len(contrasena) <= 128:
        raise ValueError("La contraseña debe tener entre 10 y 128 caracteres.")
    if not any(c.isalpha() for c in contrasena) or not any(c.isdigit() for c in contrasena):
        raise ValueError("La contraseña debe incluir al menos una letra y un número.")
    return contrasena


def generar_hash(contrasena):
    validar_contrasena(contrasena)
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), salt, ITERACIONES)
    return f"pbkdf2_sha256${ITERACIONES}${salt.hex()}${digest.hex()}"


def verificar_hash(contrasena, almacenado):
    try:
        algoritmo, rondas, salt_hex, digest_hex = almacenado.split("$")
        if algoritmo != "pbkdf2_sha256":
            return False
        rondas = int(rondas)
        if not 100_000 <= rondas <= 2_000_000:
            return False
        calculado = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), bytes.fromhex(salt_hex), rondas)
        return hmac.compare_digest(calculado.hex(), digest_hex)
    except (ValueError, TypeError, AttributeError):
        return False


def exigir_sesion(usuario):
    """Impide ejecutar operaciones sensibles sin usuario autenticado válido."""
    if not isinstance(usuario, dict) or not isinstance(usuario.get("id"), int) or usuario.get("rol") not in {"administrador", "empleado"}:
        raise PermissionError("Debes iniciar sesión para utilizar esta función.")


def exigir_administrador(usuario):
    exigir_sesion(usuario)
    if usuario.get("rol") != "administrador":
        raise PermissionError("Esta operación requiere permisos de administrador.")
