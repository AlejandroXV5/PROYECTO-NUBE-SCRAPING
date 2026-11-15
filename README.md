<!-- local-development:start -->
## Desarrollo local

Consulta [RUNNING.md](RUNNING.md) para ubicar cada componente, abrirlo en su IDE, compilarlo y conocer las comprobaciones realizadas y los requisitos pendientes.
<!-- local-development:end -->

==============================================================
        💻 PROYECTO DE SCRAPING DINÁMICO Y ESTÁTICO CON POSTGRESQL + AZURE OPENAI
==============================================================

Autor: Alejandro Bolaños Chinchilla
Carrera: Ingeniería en Tecnologías de la Información y Comunicación
Proyecto Final: Web Scraping Inteligente con LLM + Dashboard + API REST

--------------------------------------------------------------
🛠 DESCRIPCIÓN GENERAL
--------------------------------------------------------------
Este proyecto realiza scraping de sitios web dinámicos (JavaScript) y estáticos (HTML),
almacena los datos en PostgreSQL, genera archivos JSON para el frontend y utiliza Azure OpenAI (LLM)
para generar y analizar selectores CSS/XPath automáticamente.

Incluye además:
- Scheduler automático cada 30 minutos
- Logs estructurados en JSON
- API REST en Flask para exponer los datos

--------------------------------------------------------------
📦 ESTRUCTURA DEL PROYECTO
--------------------------------------------------------------

├── api/
│   └── json_api_server.py
├── data/
│   ├── events.json
│   ├── files.json
│   └── results.json
├── docs/
│   └── GUIA_INICIO.txt
├── downloads/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── main.js
│   ├── files.js
│   ├── results.js
│   └── calendar.js
├── llm/
│   └── llm_selector.py
├── logs/
│   └── scraper.log
├── scraper/
│   ├── scraper_dynamic.py
│   ├── scraper_static.py
│   └── driver/chromedriver.exe
├── scheduler.py
├── main.py
├── requirements.txt
├── .env
└── README.md

--------------------------------------------------------------
⚙️ REQUISITOS
--------------------------------------------------------------
- Python 3.9 o superior
- PostgreSQL 12 o superior
- Cuenta en Azure OpenAI con modelo gpt-4o-mini
- Google Chrome + chromedriver compatible

--------------------------------------------------------------
🧪 INSTALACIÓN Y CONFIGURACIÓN RÁPIDA
--------------------------------------------------------------

1) Clona el repositorio:
git clone https://github.com/AlejandroXV5/PROYECTO-NUBE.git
cd scraping-proyecto

2) Crea y activa el entorno virtual:
Windows:
    python -m venv venv
    venv\Scripts\activate

Linux/Mac:
    python3 -m venv venv
    source venv/bin/activate

3) Instala las dependencias:
pip install -r requirements.txt

4) Crea el archivo ".env" con tus variables:
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
🚀 USO
--------------------------------------------------------------
Acción                          | Comando
--------------------------------|------------------------------------------
Scraping Estático               | python scraper/scraper_static.py
Scraping Dinámico               | python scraper/scraper_dynamic.py
API REST Flask                  | python api/json_api_server.py
La API se ejecuta en:           | http://127.0.0.1:5000/api/productos
Dashboard Web                   | Ir a la carperta frontend, ejecutar el index.html con open live server y la API tiene que estar funcionando
Generar Backup                  | python utils\backup_db.py
Generar Selectores con LLM (IA) | python llm/llm_selector.py
Scheduler (cada 30 min)         | python scheduler.py

--------------------------------------------------------------
🧠 INTELIGENCIA ARTIFICIAL
--------------------------------------------------------------
Se utiliza Azure OpenAI (gpt-4o-mini) para:
- Generar selectores CSS/XPath automáticamente
- Analizar productos y datos scrapeados
- Realizar pruebas interactivas desde consola

--------------------------------------------------------------
🧩 AUTOMATIZACIÓN
--------------------------------------------------------------
Con APScheduler, el scraping se ejecuta automáticamente cada 30 minutos,
registrando logs y actualizando el dashboard y los archivos JSON.

--------------------------------------------------------------
📊 LOGS Y OBSERVABILIDAD
--------------------------------------------------------------
Los registros se guardan en logs/scraper.log en formato JSON estructurado
con niveles: INFO, WARNING y ERROR.

--------------------------------------------------------------
📁 BASE DE DATOS
--------------------------------------------------------------
Se usa PostgreSQL con dos tablas principales:
- productos: productos scrapeados
- downloaded_files: archivos descargados con hash y fecha

--------------------------------------------------------------
✅ CRÉDITOS
--------------------------------------------------------------
Este proyecto fue desarrollado por Alejandro Bolaños Chinchilla como parte del curso
de Computación en la Nube, en la Universidad Técnica Nacional (UTN), Grupo 1.

--------------------------------------------------------------
📤 REPOSITORIO EN GITHUB
--------------------------------------------------------------
Disponible en:
https://github.com/AlejandroXV5/PROYECTO-NUBE

==============================================================
