# -*- coding: utf-8 -*-
import traceback
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

# === Importar módulos del proyecto ===
from scraper.scraper_static import (
    scrape_static,
    save_to_db,
    exportar_a_json as exportar_json_static,
    exportar_eventos as eventos_static
)
from scraper.scraper_dynamic import (
    scrape_dynamic,
    exportar_a_json as exportar_json_dynamic,
    exportar_archivos,
    exportar_eventos as eventos_dynamic
)
from utils.backup_db import backup_db

# ✅ Importar IA
from llm.llm_selector import analizar_productos  # Asegúrate de que esta función exista

# === Configuración del Logger ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def run_full_execution():
    """
    ✅ Orquesta todo el flujo:
    1. Scraping estático
    2. Scraping dinámico
    3. Generación de JSONs
    4. Backup automático de la base de datos
    5. Análisis con LLM
    """
    logger.info("=== 🚀 START: Full scraping system execution ===")

    try:
        # 1️⃣ SCRAPING ESTÁTICO
        logger.info("▶️ Iniciando scraping estático...")
        libros = scrape_static()
        if libros:
            save_to_db(libros)
            exportar_json_static()
            eventos_static()
            logger.info("✅ Scraping estático completado.")

        # 2️⃣ SCRAPING DINÁMICO
        logger.info("▶️ Iniciando scraping dinámico...")
        scrape_dynamic()
        exportar_json_dynamic()
        exportar_archivos()
        eventos_dynamic()
        logger.info("✅ Scraping dinámico completado.")

        # 3️⃣ BACKUP DE LA BASE DE DATOS
        logger.info("💾 Generando respaldo de la base de datos...")
        backup_db()
        logger.info("✅ Respaldo de base de datos generado correctamente.")

        # 4️⃣ ANÁLISIS CON LLM
        try:
            logger.info("🧠 Ejecutando análisis con LLM...")
            analizar_productos()
            logger.info("✅ Análisis con LLM finalizado exitosamente.")
        except Exception as e:
            logger.warning("⚠️ Ocurrió un error al ejecutar el análisis con IA.")
            traceback.print_exc()

        logger.info("=== ✅ END: Full scraping system execution ===")

    except Exception as e:
        logger.error("❌ ERROR CRÍTICO durante la ejecución completa.")
        traceback.print_exc()


def start_scheduler():
    """✅ Inicia el scheduler cada 30 minutos"""
    scheduler = BlockingScheduler()
    scheduler.add_job(run_full_execution, 'interval', minutes=30)
    logger.info("⏳ Scheduler iniciado. Scraping cada 30 minutos.")
    run_full_execution()  # Ejecutar inmediatamente
    logger.info("⚡ Esperando próxima ejecución...")
    scheduler.start()


if __name__ == "__main__":
    logger.info("🔄 Lanzando ejecución completa del sistema...")
    start_scheduler()
