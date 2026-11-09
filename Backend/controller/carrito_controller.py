from fastapi import APIRouter, HTTPException, status

from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.carrito import AgregarItem, CambiarCantidad, CarritoRead
from services import carrito_service

router = APIRouter(tags=["Carrito"], prefix="/carrito")


@router.get("/", response_model=CarritoRead)
def ver(usuario: CurrentUser, session: SessionDep):
    return carrito_service.ver_carrito(usuario, session)


@router.post("/items", response_model=CarritoRead)
def agregar(data: AgregarItem, usuario: CurrentUser, session: SessionDep):
    mensaje = carrito_service.agregar_item(usuario, data, session)

    if mensaje:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje
        )

    return carrito_service.ver_carrito(usuario, session)


@router.put("/items/{id_item}", response_model=CarritoRead)
def cambiar(
    id_item: int,
    data: CambiarCantidad,
    usuario: CurrentUser,
    session: SessionDep
):
    mensaje = carrito_service.cambiar_cantidad(usuario, id_item, data, session)

    if mensaje:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje
        )

    return carrito_service.ver_carrito(usuario, session)


@router.delete("/items/{id_item}", response_model=CarritoRead)
def quitar(id_item: int, usuario: CurrentUser, session: SessionDep):
    mensaje = carrito_service.quitar_item(usuario, id_item, session)

    if mensaje:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje
        )

    return carrito_service.ver_carrito(usuario, session)
