from pydantic import BaseModel

class BubbleTeaBase(BaseModel):
    name: str
    temperature: int
    precio: int
    active: bool = True

