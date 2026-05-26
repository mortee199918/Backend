import os
import pymysql
from dotenv import load_dotenv

# Carga el archivo .env para que os.getenv funcione
load_dotenv()
conn = None  # Variable global para la conexión

def get_db_connection():
    global conn
    if conn is None:
        conn = pymysql.connect(
          charset=os.getenv("CHARSET", "utf8mb4"),
          connect_timeout=int(os.getenv("CONNECTION_TIMEOUT", 10)),
      db=os.getenv("DB", ""),
      host=os.getenv("HOST", ""),
      password=os.getenv("PASSWORD", ""),
    read_timeout=int(os.getenv("READ_TIMEOUT", 10)),
    port=int(os.getenv("PORT", 0)),  # <-- ¡Importante el int() aquí también!
    user=os.getenv("USER", ""),
    write_timeout=int(os.getenv("WRITE_TIMEOUT", 10))
)
    return conn