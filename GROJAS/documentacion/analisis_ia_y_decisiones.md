# Registro de uso de IA, análisis crítico y refactorización

**Proyecto:** EcoTech Solutions – TI3021, Unidad 3  
**Herramienta de apoyo:** ChatGPT (OpenAI), utilizada como apoyo para revisar requisitos, proponer estructura y detectar riesgos.  
**Responsabilidad:** el estudiante debe ejecutar las pruebas, revisar el código y poder explicar cada decisión antes de entregar.

## 1. Alcance del apoyo de IA
Se utilizó IA como apoyo para:
- Descomponer las rúbricas 3.1.1 a 3.1.4 en tareas verificables.
- Proponer el uso de `requests` para las solicitudes HTTP y `json`/`Response.json()` para procesar respuestas.
- Revisar validaciones de entradas, almacenamiento de contraseñas, control de acceso y manejo de excepciones.
- Proponer pruebas unitarias simuladas y documentación de instalación en VS Code.

## 2. Prompts representativos utilizados
1. «Revisa el proyecto Python EcoTech existente y conserva el CRUD de empleados. Incorpora consumo de APIs externas, autenticación segura, roles, persistencia y manejo de errores conforme a la rúbrica TI3021 Unidad 3».
2. «Analiza los riesgos de almacenar contraseñas en texto plano y propón una solución con hash, salt y comparación segura usando herramientas de Python».
3. «Diseña un cliente HTTP con Requests que gestione timeout, errores de conexión, códigos HTTP y respuestas JSON malformadas sin exponer información sensible».
4. «Propón pruebas unitarias con unittest y mocks para validar respuestas JSON y fallos de API sin depender de Internet».

Estos prompts se incluyen como evidencia representativa del proceso de apoyo; deben complementarse con capturas o historial real de la interacción si el docente solicita evidencia original.

## 3. Revisión crítica: problemas identificados y ajustes

| Código o enfoque inicial | Riesgo o limitación detectada | Decisión/refactorización aplicada |
|---|---|---|
| Contraseña comparada directamente con un valor almacenado | Podía implicar texto plano o comparación insegura | Se almacena PBKDF2-HMAC-SHA256 con salt aleatorio y se compara con `hmac.compare_digest`. |
| Usuario en memoria como único control | Se perdía al cerrar el programa | Se implementó persistencia de usuarios en SQLite y autenticación por correo. |
| Validación de correo mediante comprobar solo `@` | Aceptaba formatos incorrectos | Se incorporó validación por expresión regular y normalización a minúsculas. |
| Solicitudes HTTP sin timeout explícito | Podían quedar esperando demasiado | Se configuró timeout de conexión y lectura `(5, 12)`. |
| Procesar JSON suponiendo que siempre tiene las claves | Una respuesta incompleta podía provocar errores | Se verifican tipo de raíz, claves, tipos numéricos y rangos antes de utilizar datos. |
| Capturar todas las excepciones y mostrar el error original | Podía ocultar defectos y exponer rutas/detalles | Se capturan excepciones esperadas por categoría y se muestran mensajes seguros. |
| Consultas API disponibles desde el menú sin verificación adicional | Riesgo de ejecución fuera de una sesión válida | Se exige usuario autenticado en la función de consulta y en el cliente API. |
| SQL construido concatenando texto (riesgo general) | Posible inyección SQL | Las operaciones DAO usan consultas parametrizadas. |
| Distribuir bases de datos y bytecode del equipo de desarrollo | Podía incluir datos locales y archivos no portables | Se excluyen `.db`, `__pycache__` y `.pyc`; SQLite se crea al ejecutar. |

## 4. Justificación técnica
- **Requests:** librería ampliamente utilizada para HTTP en Python. Permite parámetros, encabezados, timeout y tratamiento de errores de respuesta.
- **Mindicador y Open-Meteo:** APIs públicas sin llave para el alcance académico, evitando incorporar credenciales secretas ficticias o innecesarias.
- **PBKDF2-HMAC-SHA256:** función de derivación de claves de la biblioteca estándar. El salt aleatorio evita hashes idénticos para contraseñas iguales; `compare_digest` reduce riesgos de comparación por tiempo.
- **SQLite:** persistencia local sin servidor adicional. Las consultas parametrizadas protegen los datos ingresados.
- **Validación antes de persistir:** evita guardar valores incompletos, con tipos incorrectos o fuera de rango.
- **Errores específicos y mensajes controlados:** permite continuidad y entrega información útil sin mostrar trazas, rutas o secretos al usuario.

## 5. Pruebas que deben ejecutarse y evidenciarse
1. Crear primer administrador e iniciar sesión correctamente.
2. Intentar iniciar sesión con contraseña incorrecta.
3. Registrar una cuenta de empleado e iniciar sesión con ella.
4. Comprobar que un empleado no visualiza ni ejecuta opciones administrativas.
5. Consultar dólar y verificar valor, unidad y fecha.
6. Consultar clima con una ciudad válida y verificar temperatura, humedad y código.
7. Consultar una ciudad inexistente y observar mensaje controlado.
8. Desconectar Internet y verificar que el programa no se cierre abruptamente.
9. Ejecutar pruebas automáticas: `python -m unittest discover -s pruebas -v`.

## 6. Limitaciones conocidas y mejoras futuras
Este programa es un prototipo académico de consola. El diccionario de usuario autenticado representa el contexto de sesión dentro del proceso local; no es un token criptográfico ni debe reutilizarse como mecanismo de sesión para una aplicación expuesta en red. Para producción se añadirían limitación de intentos, expiración de sesión, auditoría, gestión centralizada de secretos y controles de autorización a nivel de servicio. Los endpoints públicos utilizados no requieren claves API.

**Declaración:** la IA fue apoyo de desarrollo. El estudiante debe ejecutar las pruebas, revisar el comportamiento y adaptar esta documentación a las acciones que efectivamente realizó y puede explicar.
