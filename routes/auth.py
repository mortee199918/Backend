# routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import pymysql
from utils.db_connection import get_db_connection

router = APIRouter(prefix="/auth", tags=["Autenticación y Sincronización"])

# Estructura exacta de los datos que envías en 'payloadToBackend' desde Angular
class UserRegisterSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    address: str
    firebase_uid: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=201)
def register_user_in_db(user_data: UserRegisterSchema):
    """Recibe el UID de Firebase y los datos del formulario para guardarlos en MySQL"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Asegúrate de tener una tabla llamada 'usuarios' (o como prefieras) en tu MySQL de Aiven
            sql = """
                INSERT INTO usuarios (name, surname, email, phone, address, firebase_uid) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                user_data.name, 
                user_data.surname, 
                user_data.email, 
                user_data.phone, 
                user_data.address, 
                user_data.firebase_uid
            )
            cur.execute(sql, valores)
        conn.commit()
        return {"ok": True, "message": "Usuario sincronizado correctamente en MySQL"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar usuario en MySQL: {str(e)}")

@router.post("/login")
def login_user_backend(credentials: UserLoginSchema):
    """
    Como ya te has logueado en Firebase, aquí puedes verificar si el usuario existe 
    en tu BD o simplemente devolver un token JWT propio si lo necesitas.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (credentials.email,))
            user = cur.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="El usuario no está registrado en el backend")
            
            # Devolvemos una respuesta simulando el token para que Angular no rompa al leer 'response.token'
            return {
                "token": "token_falso_creado_por_el_backend_jwt", 
                "user": user
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))