from fastapi import APIRouter, HTTPException, Query, status

from db.database import SessionDep
from dependencies.auth import AdminUser
from schemas.producto import ProductoCreate, ProductoRead
from services import producto_service

router = APIRouter(tags=["Productos"], prefix="/productos")


@router.get("/", response_model=list[ProductoRead])
def listar(session: SessionDep):
    return producto_service.listar_productos(session)


@router.get("/buscar", response_model=list[ProductoRead])
def buscar(
    session: SessionDep,
    texto: str | None = Query(default=None),
    categoria_id: int | None = Query(default=None)
):
    return producto_service.buscar_productos(texto, categoria_id, session)


@router.get("/aleatorios", response_model=list[ProductoRead])
def aleatorios(
    session: SessionDep,
    cantidad: int = Query(default=4, ge=1, le=12)
):
    return producto_service.productos_aleatorios(cantidad, session)


@router.get("/categoria/{id_categoria}", response_model=list[ProductoRead])
def por_categoria(id_categoria: int, session: SessionDep):
    return producto_service.productos_de_categoria(id_categoria, session)


@router.get("/{id_producto}", response_model=ProductoRead)
def obtener(id_producto: int, session: SessionDep):
    producto = producto_service.obtener_producto(id_producto, session)

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear(data: ProductoCreate, admin: AdminUser, session: SessionDep):
    resultado = producto_service.crear_producto(data, session)

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado


@router.put("/{id_producto}", response_model=ProductoRead)
def actualizar(
    id_producto: int,
    data: ProductoCreate,
    admin: AdminUser,
    session: SessionDep
):
    resultado = producto_service.actualizar_producto(id_producto, data, session)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado


@router.delete("/{id_producto}")
def eliminar(id_producto: int, admin: AdminUser, session: SessionDep):
    resultado = producto_service.eliminar_producto(id_producto, session)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return {"mensaje": "Producto eliminado correctamente"}
