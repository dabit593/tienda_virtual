from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import crear_token
from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.usuario import Token, UsuarioCreate, UsuarioPublic
from services import auth_service

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def registrar(data: UsuarioCreate, session: SessionDep):
    resultado = auth_service.registrar_usuario(data, session)

    if isinstance(resultado, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado
        )

    return resultado


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    usuario = auth_service.autenticar_usuario(
        data.username,
        data.password,
        session
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = crear_token({"sub": usuario.correo})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UsuarioPublic)
def yo(usuario: CurrentUser):
    return usuario
