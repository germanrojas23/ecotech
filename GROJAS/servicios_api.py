"""Consumo de APIs públicas con Requests, validación JSON y errores controlados."""
import math
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from dependencia.seguridad import validar_texto, exigir_sesion

TIMEOUT = (5, 12)  # timeout de conexión y lectura (segundos)
HEADERS = {"User-Agent": "EcoTechSolutions-TI3021/1.0"}

class ErrorServicioAPI(Exception):
    """Fallo controlado al consultar o interpretar una API externa."""


def _obtener_json(url, params=None):
    try:
        respuesta = requests.get(url, params=params, timeout=TIMEOUT, headers=HEADERS)
        if respuesta.status_code == 404:
            raise ErrorServicioAPI("El recurso solicitado no existe (HTTP 404).")
        if respuesta.status_code == 429:
            raise ErrorServicioAPI("El servicio limitó las consultas (HTTP 429). Intenta más tarde.")
        respuesta.raise_for_status()
        try:
            datos = respuesta.json()
        except requests.exceptions.JSONDecodeError:
            raise ErrorServicioAPI("La API respondió con contenido que no es JSON válido.") from None
        if not isinstance(datos, dict):
            raise ErrorServicioAPI("La estructura JSON recibida no es la esperada.")
        return datos
    except Timeout:
        raise ErrorServicioAPI("La consulta superó el tiempo de espera. Intenta nuevamente.") from None
    except ConnectionError:
        raise ErrorServicioAPI("No fue posible conectar con el servicio. Revisa Internet.") from None
    except HTTPError as exc:
        codigo = exc.response.status_code if exc.response is not None else "desconocido"
        raise ErrorServicioAPI(f"El servicio respondió con un error HTTP ({codigo}).") from None
    except RequestException:
        raise ErrorServicioAPI("Ocurrió un problema de comunicación con el servicio externo.") from None


def consultar_tipo_cambio(usuario):
    """Consulta USD/CLP en Mindicador. Requiere sesión autenticada."""
    exigir_sesion(usuario)
    datos = _obtener_json("https://mindicador.cl/api")
    dolar = datos.get("dolar")
    if not isinstance(dolar, dict):
        raise ErrorServicioAPI("La API no entregó el indicador dólar.")
    valor = dolar.get("valor")
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not math.isfinite(valor) or valor <= 0:
        raise ErrorServicioAPI("El valor del dólar recibido no es válido.")
    return {"servicio": "Mindicador", "indicador": "Dólar observado", "codigo": "USD",
            "valor": float(valor), "unidad": "CLP", "fecha": str(dolar.get("fecha", ""))[:10]}


def consultar_clima(ciudad, usuario):
    """Geocodifica una ciudad y consulta condiciones actuales en Open-Meteo."""
    exigir_sesion(usuario)
    ciudad = validar_texto(ciudad, "La ciudad", 80)
    if not all(c.isalpha() or c in " -'áéíóúÁÉÍÓÚñÑüÜ" for c in ciudad):
        raise ValueError("La ciudad contiene caracteres no permitidos.")
    geo = _obtener_json("https://geocoding-api.open-meteo.com/v1/search",
                        {"name": ciudad, "count": 1, "language": "es", "format": "json"})
    resultados = geo.get("results")
    if not isinstance(resultados, list) or not resultados:
        raise ErrorServicioAPI("No se encontró la ciudad indicada.")
    lugar = resultados[0]
    try:
        lat, lon = float(lugar["latitude"]), float(lugar["longitude"])
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError
    except (KeyError, TypeError, ValueError):
        raise ErrorServicioAPI("La API de ubicación entregó coordenadas inválidas.") from None
    clima = _obtener_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "timezone": "auto"})
    actual = clima.get("current")
    if not isinstance(actual, dict):
        raise ErrorServicioAPI("La API climática no entregó condiciones actuales.")
    temp, humedad, codigo = actual.get("temperature_2m"), actual.get("relative_humidity_2m"), actual.get("weather_code")
    if (isinstance(temp, bool) or not isinstance(temp, (int, float)) or not math.isfinite(temp)
        or isinstance(humedad, bool) or not isinstance(humedad, int) or not 0 <= humedad <= 100
        or isinstance(codigo, bool) or not isinstance(codigo, int)):
        raise ErrorServicioAPI("La respuesta climática contiene valores inválidos.")
    return {"servicio": "Open-Meteo", "ciudad": str(lugar.get("name", ciudad))[:80],
            "pais": str(lugar.get("country", ""))[:80], "temperatura_c": float(temp),
            "humedad_pct": humedad, "codigo_clima": codigo, "hora": str(actual.get("time", ""))[:30]}
