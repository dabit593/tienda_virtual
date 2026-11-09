from sqlmodel import select

from models.carrito import Carrito, CarritoItem
from models.producto import Producto
from schemas.carrito import AgregarItem, CambiarCantidad, CarritoItemRead, CarritoRead


def obtener_o_crear_carrito(usuario, session):
    carrito = session.exec(
        select(Carrito).where(Carrito.usuario_id == usuario.id)
    ).first()

    if carrito is None:
        carrito = Carrito(usuario_id=usuario.id)
        session.add(carrito)
        session.commit()
        session.refresh(carrito)

    return carrito


def armar_carrito(carrito, session):
    consulta = select(CarritoItem).where(CarritoItem.carrito_id == carrito.id)
    items = session.exec(consulta).all()
    leidos = []
    total = 0

    for item in items:
        producto = session.get(Producto, item.producto_id)
        if producto is None:
            continue

        subtotal = round(item.cantidad * producto.precio, 2)
        total = round(total + subtotal, 2)
        imagen = producto.imagen
        if not imagen.startswith("/assets/"):
            imagen = "/assets/" + imagen

        leidos.append(
            CarritoItemRead(
                id=item.id,
                producto_id=producto.id,
                nombre=producto.nombre,
                precio=producto.precio,
                imagen=imagen,
                cantidad=item.cantidad,
                subtotal=subtotal,
                stock=producto.stock
            )
        )

    return CarritoRead(id=carrito.id, items=leidos, total=total)


def ver_carrito(usuario, session):
    carrito = obtener_o_crear_carrito(usuario, session)
    return armar_carrito(carrito, session)


def agregar_item(usuario, data: AgregarItem, session):
    producto = session.get(Producto, data.producto_id)

    if producto is None:
        return "El producto no existe"

    carrito = obtener_o_crear_carrito(usuario, session)
    existente = session.exec(
        select(CarritoItem).where(CarritoItem.carrito_id == carrito.id)
    ).all()

    actual = None
    for item in existente:
        if item.producto_id == producto.id:
            actual = item

    cantidad_nueva = data.cantidad
    if actual is not None:
        cantidad_nueva = actual.cantidad + data.cantidad

    if cantidad_nueva > producto.stock:
        return "No hay stock suficiente"

    if actual is None:
        actual = CarritoItem(
            carrito_id=carrito.id,
            producto_id=producto.id,
            cantidad=data.cantidad
        )
    else:
        actual.cantidad = cantidad_nueva

    session.add(actual)
    session.commit()

    return None


def cambiar_cantidad(usuario, id_item: int, data: CambiarCantidad, session):
    carrito = obtener_o_crear_carrito(usuario, session)
    item = session.get(CarritoItem, id_item)

    if item is None or item.carrito_id != carrito.id:
        return "Ese producto no está en el carrito"

    producto = session.get(Producto, item.producto_id)

    if producto is None:
        return "El producto no existe"

    if data.cantidad > producto.stock:
        return "No hay stock suficiente"

    item.cantidad = data.cantidad
    session.add(item)
    session.commit()

    return None


def quitar_item(usuario, id_item: int, session):
    carrito = obtener_o_crear_carrito(usuario, session)
    item = session.get(CarritoItem, id_item)

    if item is None or item.carrito_id != carrito.id:
        return "Ese producto no está en el carrito"

    session.delete(item)
    session.commit()

    return None
