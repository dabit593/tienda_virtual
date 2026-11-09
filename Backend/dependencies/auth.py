import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from db.database import SessionDep
from core.config import SECRET_KEY, ALGORITHM
from models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False
)


def obtener_usuario_actual(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    session: SessionDep
):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No has iniciado sesión",
            headers={"WWW-Authenticate": "Bearer"}
        )

    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la autenticación",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo = payload.get("sub")
        if correo is None:
            raise error
    except jwt.InvalidTokenError:
        raise error

    usuario = session.exec(
        select(Usuario).where(Usuario.correo == correo)
    ).first()

    if usuario is None:
        raise error

    return usuario


def obtener_admin(usuario: Annotated[Usuario, Depends(obtener_usuario_actual)]):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para esta acción"
        )

    return usuario


CurrentUser = Annotated[Usuario, Depends(obtener_usuario_actual)]
AdminUser = Annotated[Usuario, Depends(obtener_admin)]
