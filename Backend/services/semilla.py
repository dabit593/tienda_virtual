from sqlmodel import select

from core.security import hash_password
from models.carrito import Carrito
from models.categoria import Categoria
from models.producto import Producto
from models.usuario import Usuario


def cargar_datos(session):
    if session.exec(select(Categoria)).first() is None:
        tecnologia = Categoria(
            nombre="Tecnología",
            descripcion="Accesorios para estudiar y trabajar"
        )
        ropa = Categoria(
            nombre="Ropa",
            descripcion="Prendas básicas para el día a día"
        )
        hogar = Categoria(
            nombre="Hogar",
            descripcion="Cosas útiles para la casa"
        )
        session.add(tecnologia)
        session.add(ropa)
        session.add(hogar)
        session.commit()
        session.refresh(tecnologia)
        session.refresh(ropa)
        session.refresh(hogar)

        productos = [
            Producto(
                nombre="Audífonos inalámbricos",
                descripcion="Audífonos con batería para clases y música.",
                precio=24.99,
                stock=12,
                imagen="audifonos.jpg",
                categoria_id=tecnologia.id
            ),
            Producto(
                nombre="Mouse óptico",
                descripcion="Mouse con cable, cómodo para la computadora.",
                precio=9.50,
                stock=20,
                imagen="mouse.jpg",
                categoria_id=tecnologia.id
            ),
            Producto(
                nombre="Teclado USB",
                descripcion="Teclado en español para escribir tareas.",
                precio=18.00,
                stock=8,
                imagen="teclado.jpg",
                categoria_id=tecnologia.id
            ),
            Producto(
                nombre="Camiseta básica",
                descripcion="Camiseta de algodón, talla M.",
                precio=12.00,
                stock=15,
                imagen="camiseta.jpg",
                categoria_id=ropa.id
            ),
            Producto(
                nombre="Gorra",
                descripcion="Gorra de tela, ajustable.",
                precio=8.50,
                stock=10,
                imagen="gorra.jpg",
                categoria_id=ropa.id
            ),
            Producto(
                nombre="Mochila",
                descripcion="Mochila con espacio para el portátil.",
                precio=29.00,
                stock=6,
                imagen="mochila.jpg",
                categoria_id=ropa.id
            ),
            Producto(
                nombre="Taza de cerámica",
                descripcion="Taza de 300 ml para café o té.",
                precio=6.00,
                stock=25,
                imagen="taza.jpg",
                categoria_id=hogar.id
            ),
            Producto(
                nombre="Lámpara de escritorio",
                descripcion="Lámpara pequeña para leer de noche.",
                precio=22.00,
                stock=4,
                imagen="lampara.jpg",
                categoria_id=hogar.id
            ),
        ]

        for producto in productos:
            session.add(producto)

        session.commit()

    admin = session.exec(
        select(Usuario).where(Usuario.correo == "admin@mitienda.com")
    ).first()

    if admin is None:
        admin = Usuario(
            nombre="Administrador",
            correo="admin@mitienda.com",
            hashed_password=hash_password("admin1234"),
            rol="admin"
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

        carrito = Carrito(usuario_id=admin.id)
        session.add(carrito)
        session.commit()
