import random

from sqlmodel import or_, select

from models.categoria import Categoria
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoRead


def armar(producto, categoria):
    imagen = producto.imagen
    if not imagen.startswith("/assets/"):
        imagen = "/assets/" + imagen

    return ProductoRead(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        imagen=imagen,
        categoria_id=producto.categoria_id,
        categoria=categoria.nombre
    )


def consulta_con_categoria():
    consulta = select(Producto, Categoria)
    consulta = consulta.join(Categoria, Producto.categoria_id == Categoria.id)
    return consulta


def listar_productos(session):
    filas = session.exec(consulta_con_categoria()).all()
    productos = []

    for producto, categoria in filas:
        productos.append(armar(producto, categoria))

    return productos


def obtener_producto(id_producto: int, session):
    consulta = consulta_con_categoria()
    consulta = consulta.where(Producto.id == id_producto)
    fila = session.exec(consulta).first()

    if fila is None:
        return None

    producto, categoria = fila
    return armar(producto, categoria)


def buscar_productos(texto: str | None, categoria_id: int | None, session):
    consulta = consulta_con_categoria()

    if texto:
        consulta = consulta.where(
            or_(
                Producto.nombre.contains(texto),
                Producto.descripcion.contains(texto)
            )
        )

    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)

    filas = session.exec(consulta).all()
    productos = []

    for producto, categoria in filas:
        productos.append(armar(producto, categoria))

    return productos


def productos_de_categoria(id_categoria: int, session):
    return buscar_productos(None, id_categoria, session)


def productos_aleatorios(cantidad: int, session):
    productos = listar_productos(session)

    if len(productos) <= cantidad:
        return productos

    return random.sample(productos, cantidad)


def crear_producto(data: ProductoCreate, session):
    categoria = session.get(Categoria, data.categoria_id)

    if categoria is None:
        return "La categoría no existe"

    imagen = data.imagen.strip().replace("\\", "/").split("/")[-1]

    producto = Producto(
        nombre=data.nombre.strip(),
        descripcion=data.descripcion.strip(),
        precio=data.precio,
        stock=data.stock,
        imagen=imagen,
        categoria_id=data.categoria_id
    )

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return armar(producto, categoria)


def actualizar_producto(id_producto: int, data: ProductoCreate, session):
    producto = session.get(Producto, id_producto)

    if producto is None:
        return None

    categoria = session.get(Categoria, data.categoria_id)

    if categoria is None:
        return "La categoría no existe"

    imagen = data.imagen.strip().replace("\\", "/").split("/")[-1]

    producto.nombre = data.nombre.strip()
    producto.descripcion = data.descripcion.strip()
    producto.precio = data.precio
    producto.stock = data.stock
    producto.imagen = imagen
    producto.categoria_id = data.categoria_id

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return armar(producto, categoria)


def eliminar_producto(id_producto: int, session):
    from models.carrito import CarritoItem
    from models.pedido import PedidoItem

    producto = session.get(Producto, id_producto)

    if producto is None:
        return None

    en_pedidos = session.exec(
        select(PedidoItem).where(PedidoItem.producto_id == id_producto)
    ).all()

    if len(en_pedidos) > 0:
        return "No se puede eliminar el producto porque está en un pedido"

    en_carritos = session.exec(
        select(CarritoItem).where(CarritoItem.producto_id == id_producto)
    ).all()

    for item in en_carritos:
        session.delete(item)

    session.delete(producto)
    session.commit()

    return producto
