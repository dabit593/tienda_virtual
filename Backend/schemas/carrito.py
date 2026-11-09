from sqlmodel import SQLModel, Field


class AgregarItem(SQLModel):
    producto_id: int
    cantidad: int = Field(default=1, gt=0)


class CambiarCantidad(SQLModel):
    cantidad: int = Field(gt=0)


class CarritoItemRead(SQLModel):
    id: int
    producto_id: int
    nombre: str
    precio: float
    imagen: str
    cantidad: int
    subtotal: float
    stock: int


class CarritoRead(SQLModel):
    id: int
    items: list[CarritoItemRead]
    total: float
