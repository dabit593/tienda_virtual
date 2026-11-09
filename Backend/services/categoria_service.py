from sqlmodel import select

from models.categoria import Categoria
from models.producto import Producto
from schemas.categoria import CategoriaCreate


def listar_categorias(session):
    consulta = select(Categoria)
    return session.exec(consulta).all()


def obtener_categoria(id_categoria: int, session):
    return session.get(Categoria, id_categoria)


def crear_categoria(data: CategoriaCreate, session):
    repetida = session.exec(
        select(Categoria).where(Categoria.nombre == data.nombre.strip())
    ).first()

    if repetida:
        return "Ya existe una categoría con ese nombre"

    categoria = Categoria(
        nombre=data.nombre.strip(),
        descripcion=data.descripcion.strip()
    )

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


def actualizar_categoria(id_categoria: int, data: CategoriaCreate, session):
    categoria = session.get(Categoria, id_categoria)

    if categoria is None:
        return None

    repetida = session.exec(
        select(Categoria).where(Categoria.nombre == data.nombre.strip())
    ).first()

    if repetida and repetida.id != categoria.id:
        return "Ya existe una categoría con ese nombre"

    categoria.nombre = data.nombre.strip()
    categoria.descripcion = data.descripcion.strip()

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


def eliminar_categoria(id_categoria: int, session):
    categoria = session.get(Categoria, id_categoria)

    if categoria is None:
        return None

    productos = session.exec(
        select(Producto).where(Producto.categoria_id == id_categoria)
    ).all()

    if len(productos) > 0:
        return "No se puede eliminar la categoría porque tiene productos"

    session.delete(categoria)
    session.commit()

    return categoria
