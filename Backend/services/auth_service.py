from sqlmodel import select

from models.carrito import Carrito
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
from core.security import hash_password, verify_password


def correo_valido(correo: str):
    correo = correo.strip().lower()
    partes = correo.split("@")

    if len(partes) != 2 or partes[0] == "" or "." not in partes[1]:
        return None

    return correo


def registrar_usuario(data: UsuarioCreate, session):
    correo = correo_valido(data.correo)
    if correo is None:
        return "El correo no es válido"

    existente = session.exec(
        select(Usuario).where(Usuario.correo == correo)
    ).first()

    if existente:
        return "Ya existe un usuario con ese correo"

    usuario = Usuario(
        nombre=data.nombre.strip(),
        correo=correo,
        hashed_password=hash_password(data.password),
        rol="cliente"
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    carrito = Carrito(usuario_id=usuario.id)
    session.add(carrito)
    session.commit()

    return usuario


def autenticar_usuario(correo: str, password: str, session):
    correo = correo.strip().lower()

    usuario = session.exec(
        select(Usuario).where(Usuario.correo == correo)
    ).first()

    if usuario is None:
        return None

    if not verify_password(password, usuario.hashed_password):
        return None

    return usuario
