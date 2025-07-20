# ✅ API para exponer productos y archivos descargados desde PostgreSQL

from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Función para obtener productos
def get_productos():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, precio, origen, fecha_registro FROM productos ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "titulo": row[1],
            "precio": str(row[2]),
            "origen": row[3],
            "fecha_registro": row[4].strftime("%Y-%m-%d %H:%M:%S")
        })
    return data

# ✅ Función para obtener archivos
def get_archivos():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("SELECT nombre_archivo, hash_archivo, fecha_descarga FROM downloaded_files ORDER BY fecha_descarga DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "nombre_archivo": row[0],
            "hash": row[1],
            "fecha_descarga": row[2].strftime("%Y-%m-%d %H:%M:%S")
        })
    return data

# ✅ Ruta para productos
@app.route("/api/productos", methods=["GET"])
def api_productos():
    return jsonify(get_productos())

# ✅ Ruta para archivos
@app.route("/api/archivos", methods=["GET"])
def api_archivos():
    return jsonify(get_archivos())

# ✅ Ruta raíz (opcional para verificar que el servidor funciona)
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "API funcionando", "endpoints": ["/api/productos", "/api/archivos"]})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
