import openai
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar la API de OpenAI (Azure)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Clave de API de OpenAI
openai.api_base = os.getenv("OPENAI_ENDPOINT")  # Endpoint de Azure OpenAI
api_version = os.getenv("OPENAI_API_VERSION")  # Versión de la API de OpenAI
model_name = os.getenv("MODEL_NAME")  # Nombre del modelo (Ej. gpt-4, gpt-3.5, etc.)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS analisis_productos (
        id SERIAL PRIMARY KEY,
        producto_mas_caro VARCHAR(255),
        cantidad_productos INT,
        resumen TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def analizar_productos(productos):
    prompt = f"""
    Analiza esta lista de productos scrapeados y dime:
    - ¿Cuál es el producto más caro?
    - ¿Cuántos productos hay?

    Productos: {productos}
    """

    try:
        # Realizar la llamada a la API de OpenAI (Azure)
        response = openai.ChatCompletion.create(
            engine=model_name,
            api_version=api_version,
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de productos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )

        # Obtener el análisis
        analysis = response.choices[0].message["content"]
        print("Análisis generado por la IA:", analysis)

        # Aquí deberías extraer la información del análisis (esto depende de la respuesta exacta)
        producto_mas_caro = "Producto más caro extraído"  # Aquí extraerías el producto más caro del análisis
        cantidad_productos = 10  # Aquí extraerías la cantidad de productos
        resumen = "Resumen de los productos ofrecidos"  # Aquí extraerías el resumen

        # Insertar los datos en la base de datos
        cursor.execute("""
            INSERT INTO analisis_productos (producto_mas_caro, cantidad_productos, resumen)
            VALUES (%s, %s, %s)
        """, (producto_mas_caro, cantidad_productos, resumen))
        conn.commit()

        return analysis
    
    except openai.error.OpenAIError as e:
        print(f"Error al hacer la solicitud a la API de OpenAI: {e}")
        return "Error en análisis"

# Simulación de prueba local
if __name__ == "__main__":
    productos_prueba = [
        {"titulo": "Libro de Python Avanzado", "precio": "29.99", "origen": "España"},
        {"titulo": "Curso de JavaScript", "precio": "49.99", "origen": "México"},
        {"titulo": "Manual de Redes Cisco", "precio": "35.00", "origen": "EE.UU."}
    ]
    resultado = analizar_productos(productos_prueba)
    print("🧠 Análisis generado por la IA:\n", resultado)

# Cerrar la conexión
cursor.close()
conn.close()
