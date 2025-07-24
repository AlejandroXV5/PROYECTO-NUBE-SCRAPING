import openai
import os
import psycopg2
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Configurar Azure OpenAI
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

def analizar_productos():
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        # Obtener el producto más caro
        query = """
        SELECT titulo, precio
        FROM productos
        ORDER BY precio DESC
        LIMIT 1;
        """
        cursor.execute(query)
        resultado = cursor.fetchone()

        if not resultado:
            print("⚠️ No se encontró ningún producto en la base de datos.")
            return

        titulo_producto, precio = resultado
        precio = precio.replace('£', '').strip()  # Limpiar el símbolo si lo hay

        # Mostrar el producto más caro, siempre
        print(f"📦 El producto más caro es: {titulo_producto} con un precio de {precio}")

        # Prompt para Azure OpenAI
        prompt = (
            f"El producto más caro es '{titulo_producto}' con un precio de {precio} dólares. "
            "Proporcione un resumen profesional sobre este producto y su relevancia en el mercado."
        )

        # Llamada a Azure OpenAI
        try:
            response = openai.ChatCompletion.create(
                engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en análisis de productos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )

            print("🧠 Análisis generado por la IA:")
            print(response['choices'][0]['message']['content'].strip())

        except Exception as ia_error:
            print(f"⚠️ No se pudo generar análisis con IA: {ia_error}")

    except Exception as db_error:
        print(f"❌ Error de base de datos: {db_error}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# ✅ Llamar a la función si el archivo se ejecuta directamente
if __name__ == "__main__":
    analizar_productos()
