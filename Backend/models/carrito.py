from sqlmodel import SQLModel, Field


# Un usuario tiene un carrito
class Carrito(SQLModel, table=True):
    __tablename__ = "carritos"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", unique=True)


# Un carrito tiene varios productos
class CarritoItem(SQLModel, table=True):
    __tablename__ = "carrito_items"

    id: int | None = Field(default=None, primary_key=True)
    carrito_id: int = Field(foreign_key="carritos.id")
    producto_id: int = Field(foreign_key="productos.id")
    cantidad: int
