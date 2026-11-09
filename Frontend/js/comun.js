function prepararBarra() {
  const sesion = document.getElementById("sesion");
  const salir = document.getElementById("btn-salir");
  const itemSalir = document.getElementById("item-salir");
  const itemAdmin = document.getElementById("item-admin");
  const itemEntrar = document.getElementById("item-entrar");
  const itemRegistro = document.getElementById("item-registro");
  const token = leerToken();

  if (salir) {
    salir.addEventListener("click", () => {
      localStorage.removeItem("token");
      localStorage.removeItem("rol");
      localStorage.removeItem("nombre");
      window.location.href = "index.html";
    });
  }

  if (!token) {
    if (sesion) {
      sesion.textContent = "No has iniciado sesión";
    }
    if (itemSalir) {
      itemSalir.hidden = true;
    }
    if (itemAdmin) {
      itemAdmin.hidden = true;
    }
    return;
  }

  if (itemEntrar) {
    itemEntrar.hidden = true;
  }
  if (itemRegistro) {
    itemRegistro.hidden = true;
  }

  pedir("/auth/me")
    .then((usuario) => {
      localStorage.setItem("rol", usuario.rol);
      localStorage.setItem("nombre", usuario.nombre);
      if (sesion) {
        sesion.textContent = "Sesión iniciada: " + usuario.nombre;
      }
      if (itemSalir) {
        itemSalir.hidden = false;
      }
      if (itemAdmin) {
        itemAdmin.hidden = usuario.rol !== "admin";
      }
    })
    .catch(() => {
      localStorage.removeItem("token");
      localStorage.removeItem("rol");
      localStorage.removeItem("nombre");
      if (sesion) {
        sesion.textContent = "No has iniciado sesión";
      }
      if (itemSalir) {
        itemSalir.hidden = true;
      }
      if (itemAdmin) {
        itemAdmin.hidden = true;
      }
      if (itemEntrar) {
        itemEntrar.hidden = false;
      }
      if (itemRegistro) {
        itemRegistro.hidden = false;
      }
    });
}

function crearTarjeta(producto) {
  const tarjeta = document.createElement("div");
  tarjeta.className = "producto";

  const imagen = document.createElement("img");
  imagen.src = urlImagen(producto.imagen);
  imagen.alt = producto.nombre;
  imagen.className = "figura_producto";
  tarjeta.appendChild(imagen);

  const titulo = document.createElement("h3");
  titulo.textContent = producto.nombre;
  tarjeta.appendChild(titulo);

  const precio = document.createElement("p");
  precio.textContent = "Precio: " + dinero(producto.precio);
  tarjeta.appendChild(precio);

  const descripcion = document.createElement("p");
  descripcion.textContent = producto.descripcion;
  tarjeta.appendChild(descripcion);

  const stock = document.createElement("p");
  stock.textContent = "Stock: " + producto.stock;
  tarjeta.appendChild(stock);

  const enlace = document.createElement("a");
  enlace.href = "producto.html?id=" + producto.id;
  enlace.textContent = "Ver detalle";
  tarjeta.appendChild(enlace);

  return tarjeta;
}

function pintarProductos(contenedor, productos, vacio) {
  vaciar(contenedor);

  if (!productos || productos.length === 0) {
    const aviso = document.createElement("p");
    aviso.textContent = vacio;
    contenedor.appendChild(aviso);
    return;
  }

  productos.forEach((producto) => {
    contenedor.appendChild(crearTarjeta(producto));
  });
}

prepararBarra();
