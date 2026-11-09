from fastapi import APIRouter, HTTPException, status

from db.database import SessionDep
from dependencies.auth import AdminUser
from schemas.categoria import CategoriaCreate, CategoriaRead
from services import categoria_service

router = APIRouter(tags=["Categorias"], prefix="/categorias")


@router.get("/", response_model=list[CategoriaRead])
def listar(session: SessionDep):
    return categoria_service.listar_categorias(session)


@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear(data: CategoriaCreate, admin: AdminUser, session: SessionDep):
    resultado = categoria_service.crear_categoria(data, session)

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado


@router.put("/{id_categoria}", response_model=CategoriaRead)
def actualizar(
    id_categoria: int,
    data: CategoriaCreate,
    admin: AdminUser,
    session: SessionDep
):
    resultado = categoria_service.actualizar_categoria(id_categoria, data, session)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado


@router.delete("/{id_categoria}")
def eliminar(id_categoria: int, admin: AdminUser, session: SessionDep):
    resultado = categoria_service.eliminar_categoria(id_categoria, session)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return {"mensaje": "Categoría eliminada correctamente"}
