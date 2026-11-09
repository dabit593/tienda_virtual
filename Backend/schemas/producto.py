from sqlmodel import SQLModel, Field


class ProductoCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=2, max_length=300)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    imagen: str = Field(min_length=1, max_length=200)
    categoria_id: int


class ProductoRead(SQLModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    imagen: str
    categoria_id: int
    categoria: str
