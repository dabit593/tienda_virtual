from datetime import datetime

from sqlmodel import SQLModel, Field


# Un usuario puede tener varios pedidos
class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: int | None = Field(default=None, primary_key=True)
    fecha: datetime
    estado: str = Field(default="pendiente")
    total: float
    usuario_id: int = Field(foreign_key="usuarios.id")


# Un pedido guarda varios productos, con el precio de ese momento
class PedidoItem(SQLModel, table=True):
    __tablename__ = "pedido_items"

    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id")
    producto_id: int = Field(foreign_key="productos.id")
    cantidad: int
    precio_unitario: float
