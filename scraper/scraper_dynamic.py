# 🔄 Scraper dinámico de books.toscrape.com (versión final unificada)
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import logging
import requests
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import json
import hashlib

# Cargar variables de entorno
load_dotenv()

# Configurar logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s [DYNAMIC] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Crear carpetas necesarias
os.makedirs("downloads", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ✅ Crear tablas si no existen
def crear_tablas_si_no_existen():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()

        # Tabla productos
        cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            precio TEXT NOT NULL,
            origen TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """)

        # Tabla downloaded_files
        cur.execute("""
        CREATE TABLE IF NOT EXISTS downloaded_files (
            id SERIAL PRIMARY KEY,
            nombre_archivo TEXT NOT NULL,
            hash_archivo TEXT NOT NULL,
            fecha_descarga TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Tablas 'productos' y 'downloaded_files' verificadas/creadas correctamente.")
        logging.info("Tablas 'productos' y 'downloaded_files' verificadas/creadas correctamente.")
    except Exception as e:
        print(f"❌ Error creando/verificando tablas: {e}")
        logging.error(f"Error creando/verificando tablas: {e}")

# ✅ Calcular hash SHA-256 del archivo
def calcular_hash(archivo):
    sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha256.update(bloque)
    return sha256.hexdigest()

# ✅ Registrar archivo descargado en la base de datos
def registrar_archivo_bd(nombre_archivo, hash_archivo):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO downloaded_files (nombre_archivo, hash_archivo, fecha_descarga)
            VALUES (%s, %s, %s)
            """,
            (nombre_archivo, hash_archivo, datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"❌ Error al registrar archivo en BD: {e}")

# ✅ Descargar imágenes y registrar en BD
def descargar_imagen(titulo, url_imagen):
    try:
        if not url_imagen.startswith("http"):
            url_imagen = "https://books.toscrape.com/" + url_imagen.lstrip('/')
        response = requests.get(url_imagen)
        if response.status_code == 200:
            titulo_limpio = "".join(c if c.isalnum() or c in " _-" else "_" for c in titulo)
            nombre_archivo = os.path.join("downloads", f"{titulo_limpio}.jpg")
            with open(nombre_archivo, "wb") as f:
                f.write(response.content)
            hash_archivo = calcular_hash(nombre_archivo)
            registrar_archivo_bd(os.path.basename(nombre_archivo), hash_archivo)
        else:
            logging.warning(f"No se pudo descargar imagen de {titulo}: Código {response.status_code}")
    except Exception as e:
        logging.warning(f"No se pudo descargar la imagen de {titulo}: {e}")

# ✅ Guardar producto en la base de datos
def guardar_en_bd(titulo, precio):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO productos (titulo, precio, origen, fecha_registro) VALUES (%s, %s, %s, %s)",
            (titulo, precio, "scraper_dynamic", datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"❌ Error al guardar en BD (dynamic): {e}")

# ✅ Exportar productos a results.json
def exportar_a_json():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute("SELECT titulo, precio, origen, fecha_registro FROM productos ORDER BY fecha_registro DESC")
        productos = cur.fetchall()

        data = []
        for p in productos:
            data.append({
                "titulo": p[0],
                "precio": str(p[1]),
                "origen": p[2],
                "fecha": p[3].strftime("%Y-%m-%d %H:%M:%S")
            })

        with open("data/results.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✅ results.json actualizado correctamente (dynamic).")
        logging.info("results.json actualizado correctamente (dynamic).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error exportando a JSON: {e}")
        logging.error(f"Error exportando a JSON: {e}")

# ✅ Exportar archivos descargados a files.json
def exportar_archivos():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute("SELECT nombre_archivo, hash_archivo, fecha_descarga FROM downloaded_files ORDER BY fecha_descarga DESC")
        archivos = cur.fetchall()

        data = []
        for a in archivos:
            data.append({
                "nombre_archivo": a[0],
                "hash": a[1],
                "fecha_descarga": a[2].strftime("%Y-%m-%d %H:%M:%S")
            })

        with open("data/files.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✅ files.json actualizado correctamente (dynamic).")
        logging.info("files.json actualizado correctamente (dynamic).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error exportando files.json: {e}")
        logging.error(f"Error exportando files.json: {e}")

# ✅ Exportar evento a events.json
def exportar_eventos():
    eventos = [
        {
            "title": "Scraping dinámico",
            "start": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "description": "Actualización automática de productos (dynamic)"
        }
    ]
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)
    print("✅ events.json generado correctamente (dynamic).")
    logging.info("events.json generado correctamente (dynamic).")

# ✅ Scraping dinámico con Selenium
def scrape_dynamic():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://books.toscrape.com/")
        time.sleep(3)

        books = driver.find_elements(By.CLASS_NAME, "product_pod")
        for book in books:
            titulo = book.find_element(By.TAG_NAME, "h3").text.strip()
            precio = book.find_element(By.CLASS_NAME, "price_color").text.strip()
            imagen = book.find_element(By.TAG_NAME, "img").get_attribute("src")

            if not imagen.startswith("http"):
                imagen = "https://books.toscrape.com/" + imagen.lstrip('/')

            descargar_imagen(titulo, imagen)
            guardar_en_bd(titulo, precio)

        logging.info("✅ Scraping dinámico completado y datos guardados.")
        print("✅ Scraping dinámico completado y datos guardados.")
    except Exception as e:
        logging.error(f"Error durante scraping dinámico: {e}")
        print("❌ Error en scraping dinámico:", e)
    finally:
        driver.quit()

# ✅ Ejecución principal
if __name__ == "__main__":
    crear_tablas_si_no_existen()
    scrape_dynamic()
    exportar_a_json()
    exportar_archivos()
    exportar_eventos()
