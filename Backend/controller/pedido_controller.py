from fastapi import APIRouter, HTTPException, status

from db.database import SessionDep
from dependencies.auth import AdminUser, CurrentUser
from schemas.pedido import EstadoPedido, PedidoRead
from services import pedido_service

router = APIRouter(tags=["Pedidos"], prefix="/pedidos")


@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear(usuario: CurrentUser, session: SessionDep):
    resultado = pedido_service.crear_pedido(usuario, session)

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado


@router.get("/mios", response_model=list[PedidoRead])
def mios(usuario: CurrentUser, session: SessionDep):
    return pedido_service.pedidos_del_usuario(usuario, session)


@router.get("/", response_model=list[PedidoRead])
def todos(admin: AdminUser, session: SessionDep):
    return pedido_service.pedidos_todos(session)


@router.get("/{id_pedido}", response_model=PedidoRead)
def obtener(id_pedido: int, usuario: CurrentUser, session: SessionDep):
    resultado = pedido_service.obtener_pedido(id_pedido, usuario, session)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=resultado
        )

    return resultado


@router.put("/{id_pedido}/estado", response_model=PedidoRead)
def estado(
    id_pedido: int,
    data: EstadoPedido,
    admin: AdminUser,
    session: SessionDep
):
    resultado = pedido_service.cambiar_estado(id_pedido, data.estado, session)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado
