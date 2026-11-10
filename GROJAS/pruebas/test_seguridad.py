import unittest
from dependencia.seguridad import generar_hash, verificar_hash, validar_correo, validar_texto, exigir_sesion, exigir_administrador

class SeguridadTests(unittest.TestCase):
    def test_hash_no_es_texto_plano_y_verifica(self):
        clave = "EcoTech2026!"
        almacenado = generar_hash(clave)
        self.assertNotEqual(clave, almacenado)
        self.assertTrue(verificar_hash(clave, almacenado))
        self.assertFalse(verificar_hash("OtraClave2026", almacenado))

    def test_correo_invalido(self):
        with self.assertRaises(ValueError):
            validar_correo("correo-invalido")

    def test_texto_vacio(self):
        with self.assertRaises(ValueError):
            validar_texto("   ", "Ciudad")

    def test_acceso_requiere_sesion(self):
        with self.assertRaises(PermissionError):
            exigir_sesion(None)

    def test_empleado_no_es_administrador(self):
        with self.assertRaises(PermissionError):
            exigir_administrador({"id": 2, "rol": "empleado"})

if __name__ == "__main__":
    unittest.main()
