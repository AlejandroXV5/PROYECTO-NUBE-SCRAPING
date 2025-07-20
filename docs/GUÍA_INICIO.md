==============================================================
        🚀 GUÍA DE INICIO RÁPIDO – Proyecto de Scraping Inteligente
==============================================================

Autor: Alejandro Bolaños Chinchilla
Carrera: Ingeniería en Tecnologías de la Información y Comunicación
Universidad: Universidad Técnica Nacional
Modalidad: Teórico – práctico | Grupo 1
Docente: Andrés Jiménez

--------------------------------------------------------------
✅ REQUISITOS PREVIOS
--------------------------------------------------------------
Antes de comenzar, asegúrate de contar con:

- Python 3.9 o superior
- PostgreSQL 12 o superior
- Google Chrome (última versión)
- Chromedriver compatible con tu versión de Chrome
- Cuenta en Azure con acceso a Azure OpenAI y modelo gpt-4o-mini

--------------------------------------------------------------
⚙ INSTALACIÓN RÁPIDA
--------------------------------------------------------------

1) Clonar el repositorio
------------------------
git clone https://github.com/AlejandroXV5/PROYECTO-NUBE.git
cd scraping-proyecto

2) Crear y activar el entorno virtual
-------------------------------------
Windows:
    python -m venv venv
    venv\Scripts\activate

Linux/Mac:
    python3 -m venv venv
    source venv/bin/activate

3) Instalar dependencias
------------------------
pip install -r requirements.txt

4) Configurar variables de entorno
----------------------------------
Crea un archivo ".env" en la raíz con el siguiente contenido:

OPENAI_API_KEY=tu_clave_personal
OPENAI_ENDPOINT=https://voiceflip-openai.openai.azure.com/
MODEL_NAME=gpt-4o-mini
API_VERSION=2025-01-01-preview

DB_HOST=localhost
DB_PORT=5432
DB_NAME=proyectonube
DB_USER=postgres
DB_PASSWORD=1234

--------------------------------------------------------------
▶ EJECUCIÓN DEL PROYECTO
--------------------------------------------------------------

Funcionalidad                    | Comando
---------------------------------|-----------------------------------------
Scraping Estático                | python scraper/scraper_static.py
Scraping Dinámico                | python scraper/scraper_dynamic.py
API REST (JSON)                  | python api/json_api_server.py
La API se ejecuta en:            | http://127.0.0.1:5000/api/productos
Dashboard Web                    | Abrir "frontend/index.html" en el navegador
Scheduler Automático (30 min)    | python scheduler.py
Selectores con LLM (IA)          | python llm/llm_selector.py

--------------------------------------------------------------
📁 ESTRUCTURA DEL PROYECTO
--------------------------------------------------------------

├── scraper/         -> Scrapers dinámico y estático
├── llm/             -> Generador de selectores con IA (LLM)
├── api/             -> API Flask con salida JSON
├── frontend/        -> Interfaz visual (HTML, CSS y JS)
├── logs/            -> Registros del sistema en JSON
├── data/            -> Resultados exportados
├── downloads/       -> Archivos descargados
├── scheduler.py     -> Ejecución automática cada 30 min
└── .env             -> Variables sensibles (NO subir a GitHub)

--------------------------------------------------------------
🔥 NOTAS IMPORTANTES
--------------------------------------------------------------

- La API se ejecuta en: http://127.0.0.1:5000/api/productos
- El scheduler.py ejecuta scraping automático cada 30 min
- NO subas el archivo ".env" a GitHub
- Verifica siempre que chromedriver coincida con tu versión de Chrome
- El Dashboard se actualiza con los datos de: data/results.json

--------------------------------------------------------------
❗ SOPORTE TÉCNICO
--------------------------------------------------------------

Para dudas o problemas:
Contacta a Alejandro Bolaños Chinchilla
O revisa la documentación técnica en README.md

==============================================================
