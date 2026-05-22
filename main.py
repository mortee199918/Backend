from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Bubble Tea API")

# ========================================================
# 1. MODELOS DE PYDANTIC (Esquemas de datos)
# ========================================================

# Esquemas para Usuarios
class UserBase(BaseModel):
    name: str
    surname: str
    email: EmailStr

class UserCreate(UserBase):
    pass  # Se usa para recibir datos cuando se registra un usuario

class UserResponse(UserBase):
    id: int  # Cuando devolvemos el usuario, ya incluye su ID de la base de datos

    class Config:
        from_attributes = True


# Esquemas para Bubble Tea
class BubbleTeaBase(BaseModel):
    name: str
    temperature: int
    precio: int
    active: bool = True

class BubbleTeaCreate(BubbleTeaBase):
    pass

class BubbleTeaResponse(BubbleTeaBase):
    id: int

    class Config:
        from_attributes = True


# ========================================================
# 2. SIMULACIÓN DE BASE DE DATOS (Listas temporales)
# ========================================================

db_users = [
    {"id": 1, "name": "Juan", "surname": "Pérez", "email": "juan.perez@email.com"},
    {"id": 2, "name": "María", "surname": "Gómez", "email": "maria.gomez@email.com"}
]

db_bubble_teas = [
    {"id": 1, "name": "Matcha Clásico", "temperature": 1, "precio": 5, "active": True},
    {"id": 2, "name": "Taro Milk Tea", "temperature": 1, "precio": 5, "active": True}
]


# ========================================================
# 3. ENDPOINTS / PETICIONES (Rutas de la API)
# ========================================================

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Bubble Tea 🧋"}


# --- RUTAS DE USUARIOS ---

@app.get("/users", response_model=List[UserResponse])
def get_users():
    """Obtener todos los usuarios de la lista"""
    return db_users


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """Crear un nuevo usuario (Comprueba que el email no esté repetido)"""
    if any(u["email"] == user.email for u in db_users):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_usuario = {
        "id": len(db_users) + 1,
        **user.model_dump()
    }
    db_users.append(nuevo_usuario)
    return nuevo_usuario


# --- RUTAS DE BUBBLE TEA ---

@app.get("/bubble-tea", response_model=List[BubbleTeaResponse])
def get_bubble_teas(active_only: bool = False):
    """Obtener todos los Bubble Teas (o filtrar solo los activos si active_only=true)"""
    if active_only:
        return [b for b in db_bubble_teas if b["active"]]
    return db_bubble_teas


@app.get("/bubble-tea/{tea_id}", response_model=BubbleTeaResponse)
def get_bubble_tea_by_id(tea_id: int):
    """Buscar un Bubble Tea específico usando su ID"""
    for tea in db_bubble_teas:
        if tea["id"] == tea_id:
            return tea
    raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")


@app.post("/bubble-tea", response_model=BubbleTeaResponse, status_code=201)
def create_bubble_tea(tea: BubbleTeaCreate):
    """Añadir un nuevo Bubble Tea a la carta"""
    nuevo_tea = {
        "id": len(db_bubble_teas) + 1,
        **tea.model_dump()
    }
    db_bubble_teas.append(nuevo_tea)
    return nuevo_tea