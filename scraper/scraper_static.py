# 🔄 Scraper estático de books.toscrape.com (versión final unificada)
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s [STATIC] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Crear carpetas necesarias
os.makedirs("data", exist_ok=True)

# ✅ Crear tabla si no existe
def crear_tabla_si_no_existe():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            precio TEXT NOT NULL,
            origen TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Tabla 'productos' verificada/creada correctamente.")
        logging.info("Tabla 'productos' verificada/creada correctamente.")
    except Exception as e:
        print(f"❌ Error creando/verificando tabla productos: {e}")
        logging.error(f"Error creando/verificando tabla productos: {e}")

# ✅ Scraping estático con BeautifulSoup
def scrape_static():
    try:
        url = "https://books.toscrape.com/"
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        books = []
        for item in soup.select(".product_pod"):
            title = item.h3.a["title"]
            price = item.select_one(".price_color").text
            books.append({
                "title": title,
                "price": price
            })

        print(f"✅ Se encontraron {len(books)} libros (static).")
        logging.info(f"Se encontraron {len(books)} libros (static).")
        return books
    except Exception as e:
        logging.error("Error en scrape_static: %s", e)
        print("❌ Error durante scraping estático:", e)
        return []

# ✅ Guardar productos en la base de datos
def save_to_db(data):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        for item in data:
            cur.execute(
                "INSERT INTO productos (titulo, precio, origen, fecha_registro) VALUES (%s, %s, %s, %s)",
                (item["title"], item["price"], "scraper_static", datetime.now())
            )
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Datos guardados en PostgreSQL con éxito (static).")
        logging.info("Datos guardados en PostgreSQL con éxito (static).")
    except Exception as e:
        logging.error("Error al guardar en la base de datos (static): %s", e)
        print("❌ Error al guardar en la base de datos:", e)

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

        print("✅ results.json actualizado correctamente (static).")
        logging.info("results.json actualizado correctamente (static).")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error exportando a JSON: {e}")
        logging.error(f"Error exportando a JSON: {e}")

# ✅ Exportar evento a events.json
def exportar_eventos():
    eventos = [
        {
            "title": "Scraping estático ejecutado",
            "start": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "description": "Actualización automática de productos (static)"
        }
    ]
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)
    print("✅ events.json generado correctamente (static).")
    logging.info("events.json generado correctamente (static).")

# ✅ Ejecución principal
if __name__ == "__main__":
    crear_tabla_si_no_existe()
    libros = scrape_static()
    if libros:
        save_to_db(libros)
        exportar_a_json()
        exportar_eventos()
