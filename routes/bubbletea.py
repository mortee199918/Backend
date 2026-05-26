
from models.models import BubbleTeaBase
import pymysql
from fastapi import APIRouter, HTTPException
from models.models import BubbleTeaBase
from utils.db_connection import get_db_connection


router = APIRouter(prefix="/bubbleteas", tags=["Bubble Teas from Aiven"])  
conn = get_db_connection()  # Conexión global para todo el router

@router.get("/")  # O "/bubbleteas", según como lo hayas dejado
def get_bubble_teas_from_aiven():
    """Obtiene los Bubble Teas directamente desde la base de datos de Aiven"""
    try:
        # Obtenemos la conexión justo aquí dentro, al recibir la petición
        conn = get_db_connection() 
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM BubbleTea") 
            result = cursor.fetchall()
            return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

@router.get("/bubbleteas/{id}")
def get_bubble_teas_from_aiven_by_id(id: int):
    """Busca un Bubble Tea específico por su ID directamente en Aiven (solo si está activo)"""
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            # Ejecutamos la consulta pasando el id de forma segura en la tupla (id,)
            cur.execute("SELECT * FROM BubbleTea WHERE id = %s AND active = TRUE", (id,))
            row = cur.fetchone()
            
            # Si el id no existe o no está activo, row será None
            if row is None:
                raise HTTPException(status_code=404, detail="Bubble Tea no encontrado o inactivo")
                
            return {"ok": True, "result": row}
            
    except HTTPException as http_ex:
        # Re-lanzamos el error 404 para que FastAPI lo gestione correctamente
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    
@router.post("/bubbleteas", status_code=201)
def create_bubble_tea_from_aiven(bubble_tea: BubbleTeaBase):
    """Inserta un nuevo Bubble Tea en la base de datos de Aiven"""
    try:
        with conn.cursor() as cur:
            # Consulta SQL estructurada de forma segura
            sql = "INSERT INTO BubbleTea (name, temperature, precio, active) VALUES (%s, %s, %s, %s)"
            
            # Pasamos los valores directamente desde el modelo Pydantic
            valores = (bubble_tea.name, bubble_tea.temperature, bubble_tea.precio, bubble_tea.active)
            
            cur.execute(sql, valores)
            
        # ¡IMPORTANTE! Confirmamos los cambios en la base de datos
        conn.commit()
        
        return {"ok": True, "result": bubble_tea.model_dump()}
        
    except Exception as e:
        # Si algo falla, hacemos rollback para no dejar la base de datos en un estado inestable
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al insertar en la base de datos: {str(e)}")
    
@router.put("/bubbleteas/{id}")
def update_bubble_tea_from_aiven(id: int, bubble_tea: BubbleTeaBase):
    try:
        with conn.cursor() as cur:
            # Usamos "BubbleTea" o "bubbletea" según lo tengas en Workbench
            sql = """
                UPDATE BubbleTea 
                SET name = %s, temperature = %s, precio = %s, active = %s 
                WHERE id = %s
            """
            valores = (bubble_tea.name, bubble_tea.temperature, bubble_tea.precio, bubble_tea.active, id)
            cur.execute(sql, valores)
            
            # Si cur.rowcount es 0, significa que ese ID no existe en la base de datos
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"No se encontró ningún Bubble Tea con el ID {id}")
                
        conn.commit()
        return {"ok": True, "message": f"Bubble Tea con ID {id} actualizado correctamente"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        conn.rollback()
        # Esto te mostrará el error real en Postman si vuelve a fallar
        raise HTTPException(status_code=500, detail=f"Error interno en MySQL: {str(e)}")


@router.delete("/bubbleteas/{id}")
def delete_bubble_tea_from_aiven(id: int):
    """Elimina por completo un registro de Bubble Tea en Aiven"""
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM BubbleTea WHERE id = %s"
            cur.execute(sql, (id,))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Bubble Tea no encontrado para eliminar")
                
        conn.commit()
        return {"ok": True, "message": f"Bubble Tea con ID {id} eliminado de la base de datos"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar en la base de datos: {str(e)}")