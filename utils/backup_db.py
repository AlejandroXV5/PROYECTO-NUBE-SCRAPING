import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ✅ Crear carpeta de backups si no existe
os.makedirs("backups", exist_ok=True)

def backup_db():
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_respaldo = f"backups/backup_{fecha}.sql"

    try:
        # ✅ Configurar la contraseña solo para este comando
        os.environ["PGPASSWORD"] = DB_PASSWORD
        PG_DUMP_PATH = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

        # ✅ Comando pg_dump usando la ruta correcta
        comando = [
            PG_DUMP_PATH,
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-F", "p",               # Formato SQL plano
            "-f", nombre_respaldo,   # Archivo de salida
            DB_NAME
        ]

        subprocess.run(comando, check=True)
        print(f"✅ Respaldo generado correctamente: {nombre_respaldo}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar el respaldo: {e}")

    finally:
        # ✅ Eliminar la contraseña del entorno por seguridad
        os.environ.pop("PGPASSWORD", None)

if __name__ == "__main__":
    backup_db()
