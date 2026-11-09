from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from core.config import DATABASE_URL
from models.carrito import Carrito, CarritoItem
from models.categoria import Categoria
from models.pedido import Pedido, PedidoItem
from models.producto import Producto
from models.usuario import Usuario

connect_args = {}
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Se importan para que create_all cree todas las tablas
MODELOS = (Usuario, Categoria, Producto, Carrito, CarritoItem, Pedido, PedidoItem)


def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    from services.semilla import cargar_datos

    with Session(engine) as session:
        cargar_datos(session)

    yield


def obtener_sesion():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(obtener_sesion)]
