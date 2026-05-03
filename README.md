CobrApp - Automatización de Verificación de Pagos vía WhatsApp 
CobrApp es una solución integral diseñada para automatizar la validación de comprobantes de pago (Yape y Plin) recibidos a través de WhatsApp. El sistema utiliza reconocimiento óptico de caracteres (OCR) mediante inteligencia artificial para extraer datos críticos y registrarlos automáticamente en una base de datos en la nube.

Este proyecto fue desarrollado como parte del programa de Diseño y Desarrollo de Software.

Tecnologías Utilizadas
n8n: Orquestador de flujo de trabajo y automatización.

Python (FastAPI): API personalizada para el procesamiento de imágenes.

Tesseract OCR: Motor de reconocimiento de texto.

Docker & Docker-Compose: Contenedores para asegurar un entorno de ejecución consistente.

Twilio API: Integración de mensajería para WhatsApp.

Google Sheets API: Almacenamiento y registro de transacciones.

Arquitectura del Sistema
El flujo de trabajo sigue la siguiente lógica de microservicios:

Recepción: Un Webhook recibe la notificación de Twilio cuando llega una imagen por WhatsApp.

Procesamiento: El flujo descarga la imagen y la envía a un contenedor de Python.

Extracción (OCR): La API de Python pre-procesa la imagen (Escala de grises/Umbralización) y utiliza Regex avanzados para extraer Monto, Número de Operación y Fecha.

Validación: Se verifica mediante lógica booleana si los datos extraídos corresponden a un comprobante válido.

Registro: Los datos validados se insertan en una fila nueva de Google Sheets.

Instalación y Despliegue
Requisitos Previos
Docker y Docker-Compose instalados.

Cuenta de Twilio (Sandbox de WhatsApp activo).

Credenciales de Google Cloud Console para la API de Sheets.

Pasos para ejecutar
Clonar el repositorio:

Bash
git clone https://github.com/zair-l/Automatizaci-n-WhatsApp.git
cd cobrapp
Levantar los servicios con Docker:

Bash
docker-compose up --build -d
Acceder a n8n en http://localhost:5678 e importar el archivo de workflow incluido en la carpeta /workflows.

Configuración de la API de Python
El script main.py incluye un motor de búsqueda basado en expresiones regulares (Regex) capaz de identificar variantes comunes de lectura del OCR:

Identificación de símbolos de moneda: S/, s/, 5/, B/.

Soporte para montos enteros y decimales.

Detección automática de tipo de pago (Yape/Plin).

Autor
Zair Leonardo Triviño Villanueva - Estudiante de Desarrollado de Software
