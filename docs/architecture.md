==============================================================
        📐 ARQUITECTURA DEL PROYECTO
==============================================================

Nombre del Proyecto: Scraping Web Dinámico y Estático con PostgreSQL + Azure OpenAI
Autor: Alejandro Bolaños Chinchilla
Descripción: Este documento explica la arquitectura funcional del sistema desarrollado.

--------------------------------------------------------------
🔄 FLUJO GENERAL DEL SISTEMA
--------------------------------------------------------------
+------------------+      +-------------------+      +--------------------+      +------------------+
| Scrapers         | ---> | PostgreSQL DB     | ---> | JSON Files (API)   | ---> | Frontend (UI)    |
| (Dinámico y Est.)|      | productos + logs  |      | results / files    |      | Dashboard Web    |
+------------------+      +-------------------+      +--------------------+      +------------------+

                          +----------------+
                          | Azure OpenAI   |
                          | Selectores LLM |
                          +----------------+

--------------------------------------------------------------
🔧 MÓDULOS PRINCIPALES
--------------------------------------------------------------
Módulo           | Descripción
-----------------|---------------------------------------------------------------
scraper/         | Contiene scraper_dynamic.py (Selenium) y scraper_static.py (BeautifulSoup).
downloads/       | Carpeta donde se guardan los archivos descargados.
data/            | Contiene los archivos results.json, files.json, events.json para mostrar en el frontend.
llm/             | Analiza productos o genera selectores con el modelo GPT-4o desde Azure OpenAI.
logs/            | Guarda scraper.log con logs estructurados en JSON.
api/             | API REST desarrollada en Flask para consumir desde JavaScript (frontend).
frontend/        | HTML5, CSS y JS que muestran productos, archivos y eventos con fetch() y FullCalendar.js.
scheduler.py     | Programa la ejecución automática cada 30 minutos usando APScheduler.
.env             | Variables de entorno (PostgreSQL y claves de Azure).
docs/            | Guías documentación técnica.
backups/         | Contiene backups de la base de datos.

--------------------------------------------------------------
🧠 INTEGRACIÓN CON LLM (AZURE OPENAI)
--------------------------------------------------------------
- Utiliza el modelo gpt-4o-mini para:
  * Generar selectores CSS/XPath a partir de HTML.
  * Analizar productos y generar respuestas inteligentes.
- Implementado vía API REST (llm/llm_selector.py).

--------------------------------------------------------------
📊 OBSERVABILIDAD Y LOGS
--------------------------------------------------------------
- Todos los procesos (scraping, errores, cambios) se registran en logs/scraper.log.
- Formato JSON estructurado con:
  * timestamp
  * level
  * message

--------------------------------------------------------------
🔁 AUTOMATIZACIÓN
--------------------------------------------------------------
- scheduler.py ejecuta el scraping dinámico y estático cada 30 minutos.
- Actualiza automáticamente:
  * Archivos results.json y files.json
  * Base de datos proyectonube
  * Carpeta de descargas con verificación SHA-256

--------------------------------------------------------------
🔐 SEGURIDAD
--------------------------------------------------------------
- Las claves de Azure y PostgreSQL se almacenan en el archivo .env.
- No se exponen directamente en los scripts.

--------------------------------------------------------------
✅ CONCLUSIÓN
--------------------------------------------------------------
Este diseño modular permite ampliar el sistema fácilmente para nuevos sitios web,
nuevos formatos de datos o APIs adicionales.

==============================================================