# routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import pymysql
from utils.db_connection import get_db_connection

router = APIRouter(prefix="/auth", tags=["Auth & Sincronización"])

# Modelo Pydantic para validar los datos que vienen del 'register.ts' de Angular
class UserRegisterSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    address: str
    firebase_uid: str

# Modelo Pydantic para validar los datos que vienen del 'login.ts' de Angular
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=201)
def register_user_in_db(user_data: UserRegisterSchema):
    """Recibe el UID de Firebase y los datos del formulario para guardarlos en MySQL de Aiven"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # NOTA: Asegúrate de tener creada la tabla 'usuarios' en tu base de datos de Aiven
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
        return {"ok": True, "message": "Usuario sincronizado correctamente en MySQL de Aiven"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar en MySQL: {str(e)}")

@router.post("/login")
def login_user_backend(credentials: UserLoginSchema):
    """Verifica si el usuario autenticado en Firebase existe en la base de datos local"""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            sql = "SELECT * FROM usuarios WHERE email = %s"
            cur.execute(sql, (credentials.email,))
            user = cur.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="El usuario autenticado en Firebase no existe en el backend")
            
            # Devolvemos un token simulado y los datos del usuario para cumplir con lo que espera tu login.ts
            return {
                "token": "simulated_jwt_token_for_local_development", 
                "user": user
            }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")