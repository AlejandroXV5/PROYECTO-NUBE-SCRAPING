import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

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
        cur.execute("SELECT titulo, precio, url, fecha_registro FROM productos ORDER BY fecha_registro DESC")
        productos = cur.fetchall()

        data = []
        for p in productos:
            data.append({
                "titulo": p[0],
                "precio": str(p[1]),  # como texto por los símbolos £
                "origen": p[2],
                "fecha": p[3].strftime("%Y-%m-%d %H:%M:%S")
            })

        os.makedirs("data", exist_ok=True)
        with open("data/results.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✅ results.json actualizado correctamente")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error exportando a JSON: {e}")


def exportar_eventos():
    eventos = [
        {
            "title": "Scraping ejecutado",
            "start": "2025-07-18T15:00:00",
            "description": "Scraping de productos actualizado"
        }
    ]

    os.makedirs("data", exist_ok=True)
    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)

    print("✅ events.json generado correctamente")
