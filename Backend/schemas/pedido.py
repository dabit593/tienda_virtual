from datetime import datetime

from sqlmodel import SQLModel, Field


class PedidoItemRead(SQLModel):
    id: int
    producto_id: int
    nombre: str
    imagen: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class PedidoRead(SQLModel):
    id: int
    fecha: datetime
    estado: str
    total: float
    usuario_id: int
    cliente: str
    items: list[PedidoItemRead]


class EstadoPedido(SQLModel):
    estado: str
