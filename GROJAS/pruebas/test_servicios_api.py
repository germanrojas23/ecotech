import unittest
from unittest.mock import Mock, patch
import requests
from servicios_api import _obtener_json, ErrorServicioAPI, consultar_tipo_cambio

USUARIO = {"id": 1, "rol": "administrador"}

class ApiTests(unittest.TestCase):
    @patch("servicios_api.requests.get")
    def test_procesa_json(self, get):
        respuesta = Mock()
        respuesta.status_code = 200
        respuesta.json.return_value = {"dolar": {"valor": 950.5}}
        get.return_value = respuesta
        self.assertEqual(_obtener_json("https://ejemplo.test/api")["dolar"]["valor"], 950.5)
        get.assert_called_once()
        self.assertEqual(get.call_args.kwargs["timeout"], (5, 12))

    @patch("servicios_api.requests.get")
    def test_error_http_404(self, get):
        respuesta = Mock()
        respuesta.status_code = 404
        respuesta.raise_for_status.side_effect = requests.HTTPError(response=respuesta)
        get.return_value = respuesta
        with self.assertRaises(ErrorServicioAPI):
            _obtener_json("https://ejemplo.test/no-existe")

    @patch("servicios_api.requests.get", side_effect=requests.Timeout)
    def test_timeout_controlado(self, get):
        with self.assertRaisesRegex(ErrorServicioAPI, "tiempo de espera"):
            _obtener_json("https://ejemplo.test/lento")

    @patch("servicios_api._obtener_json")
    def test_extrae_tipo_cambio(self, obtener):
        obtener.return_value = {"dolar": {"valor": 950.5, "fecha": "2026-11-09"}}
        datos = consultar_tipo_cambio(USUARIO)
        self.assertEqual(datos["codigo"], "USD")
        self.assertEqual(datos["valor"], 950.5)

    def test_api_requiere_sesion(self):
        with self.assertRaises(PermissionError):
            consultar_tipo_cambio(None)

if __name__ == "__main__":
    unittest.main()
