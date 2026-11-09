from datetime import datetime, timezone

from sqlmodel import select

from models.carrito import CarritoItem
from models.pedido import Pedido, PedidoItem
from models.producto import Producto
from models.usuario import Usuario
from schemas.pedido import PedidoItemRead, PedidoRead
from services.carrito_service import obtener_o_crear_carrito

ESTADOS = ("pendiente", "procesando", "enviado", "entregado")


def armar_pedido(pedido, session):
    cliente = session.get(Usuario, pedido.usuario_id)
    nombre_cliente = cliente.nombre if cliente else ""

    consulta = select(PedidoItem).where(PedidoItem.pedido_id == pedido.id)
    items = session.exec(consulta).all()
    leidos = []

    for item in items:
        producto = session.get(Producto, item.producto_id)
        nombre = "Producto"
        imagen = ""
        if producto is not None:
            nombre = producto.nombre
            imagen = producto.imagen
            if not imagen.startswith("/assets/"):
                imagen = "/assets/" + imagen

        subtotal = round(item.cantidad * item.precio_unitario, 2)
        leidos.append(
            PedidoItemRead(
                id=item.id,
                producto_id=item.producto_id,
                nombre=nombre,
                imagen=imagen,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=subtotal
            )
        )

    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        estado=pedido.estado,
        total=pedido.total,
        usuario_id=pedido.usuario_id,
        cliente=nombre_cliente,
        items=leidos
    )


def crear_pedido(usuario, session):
    carrito = obtener_o_crear_carrito(usuario, session)
    items = session.exec(
        select(CarritoItem).where(CarritoItem.carrito_id == carrito.id)
    ).all()

    if len(items) == 0:
        return "El carrito está vacío"

    productos = []
    total = 0

    for item in items:
        producto = session.get(Producto, item.producto_id)
        if producto is None:
            return "Hay un producto del carrito que ya no existe"

        if item.cantidad > producto.stock:
            return "No hay stock suficiente de " + producto.nombre

        total = round(total + (item.cantidad * producto.precio), 2)
        productos.append((item, producto))

    pedido = Pedido(
        fecha=datetime.now(timezone.utc),
        estado="pendiente",
        total=total,
        usuario_id=usuario.id
    )

    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    for item, producto in productos:
        detalle = PedidoItem(
            pedido_id=pedido.id,
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )
        producto.stock = producto.stock - item.cantidad
        session.add(detalle)
        session.add(producto)
        session.delete(item)

    session.commit()
    session.refresh(pedido)

    return armar_pedido(pedido, session)


def pedidos_del_usuario(usuario, session):
    consulta = select(Pedido).where(Pedido.usuario_id == usuario.id)
    pedidos = session.exec(consulta).all()
    lista = []

    for pedido in pedidos:
        lista.append(armar_pedido(pedido, session))

    return lista


def pedidos_todos(session):
    pedidos = session.exec(select(Pedido)).all()
    lista = []

    for pedido in pedidos:
        lista.append(armar_pedido(pedido, session))

    return lista


def obtener_pedido(id_pedido: int, usuario, session):
    pedido = session.get(Pedido, id_pedido)

    if pedido is None:
        return None

    if usuario.rol != "admin" and pedido.usuario_id != usuario.id:
        return "No puedes ver este pedido"

    return armar_pedido(pedido, session)


def cambiar_estado(id_pedido: int, estado: str, session):
    estado = estado.strip().lower()

    if estado not in ESTADOS:
        return "El estado debe ser pendiente, procesando, enviado o entregado"

    pedido = session.get(Pedido, id_pedido)

    if pedido is None:
        return None

    pedido.estado = estado
    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    return armar_pedido(pedido, session)
