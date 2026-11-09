from sqlmodel import SQLModel, Field


# Una categoria tiene varios productos
class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: float
    stock: int = Field(default=0)
    imagen: str
    categoria_id: int = Field(foreign_key="categorias.id")
