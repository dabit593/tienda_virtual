const mensaje = document.getElementById("mensaje");
const productos = document.getElementById("tabla-productos");
const categorias = document.getElementById("tabla-categorias");
const pedidos = document.getElementById("tabla-pedidos");
const selectCategoria = document.getElementById("producto-categoria");
const formProducto = document.getElementById("form-producto");
const formCategoria = document.getElementById("form-categoria");
const bloques = [
  document.getElementById("bloque-categorias"),
  document.getElementById("bloque-productos"),
  document.getElementById("bloque-pedidos"),
];

function mostrarBloques(visible) {
  bloques.forEach((bloque) => {
    bloque.hidden = !visible;
  });
}

const estados = ["pendiente", "procesando", "enviado", "entregado"];

function celda(texto) {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function opcionCategoria(categoria) {
  const opcion = document.createElement("option");
  opcion.value = categoria.id;
  opcion.textContent = categoria.nombre;
  return opcion;
}

function cargarCategorias() {
  return pedir("/categorias").then((lista) => {
    vaciar(selectCategoria);
    vaciar(categorias);

    lista.forEach((categoria) => {
      selectCategoria.appendChild(opcionCategoria(categoria));

      const fila = document.createElement("tr");
      fila.appendChild(celda(categoria.nombre));
      fila.appendChild(celda(categoria.descripcion));

      const acciones = document.createElement("td");

      const editar = document.createElement("button");
      editar.type = "button";
      editar.textContent = "Editar";
      editar.addEventListener("click", () => {
        document.getElementById("categoria-id").value = categoria.id;
        document.getElementById("categoria-nombre").value = categoria.nombre;
        document.getElementById("categoria-descripcion").value = categoria.descripcion;
      });
      acciones.appendChild(editar);

      const borrar = document.createElement("button");
      borrar.type = "button";
      borrar.textContent = "Eliminar";
      borrar.addEventListener("click", () => {
        pedir("/categorias/" + categoria.id, { method: "DELETE" })
          .then(() => {
            mensaje.textContent = "Categoría eliminada";
            cargarCategorias();
          })
          .catch((error) => {
            mensaje.textContent = error.message;
          });
      });
      acciones.appendChild(borrar);

      fila.appendChild(acciones);
      categorias.appendChild(fila);
    });
  });
}

function cargarProductos() {
  return pedir("/productos/").then((lista) => {
    vaciar(productos);

    lista.forEach((producto) => {
      const fila = document.createElement("tr");
      fila.appendChild(celda(producto.nombre));
      fila.appendChild(celda(producto.descripcion));
      fila.appendChild(celda(producto.precio));
      fila.appendChild(celda(producto.stock));

      const acciones = document.createElement("td");

      const editar = document.createElement("button");
      editar.type = "button";
      editar.textContent = "Editar";
      editar.addEventListener("click", () => {
        document.getElementById("producto-id").value = producto.id;
        document.getElementById("producto-nombre").value = producto.nombre;
        document.getElementById("producto-descripcion").value = producto.descripcion;
        document.getElementById("producto-precio").value = producto.precio;
        document.getElementById("producto-stock").value = producto.stock;
        document.getElementById("producto-imagen").value = producto.imagen.split("/").pop();
        document.getElementById("producto-categoria").value = producto.categoria_id;
      });
      acciones.appendChild(editar);

      const borrar = document.createElement("button");
      borrar.type = "button";
      borrar.textContent = "Eliminar";
      borrar.addEventListener("click", () => {
        pedir("/productos/" + producto.id, { method: "DELETE" })
          .then(() => {
            mensaje.textContent = "Producto eliminado";
            cargarProductos();
          })
          .catch((error) => {
            mensaje.textContent = error.message;
          });
      });
      acciones.appendChild(borrar);

      fila.appendChild(acciones);
      productos.appendChild(fila);
    });
  });
}

function cargarPedidos() {
  return pedir("/pedidos/").then((lista) => {
    vaciar(pedidos);

    if (lista.length === 0) {
      const fila = document.createElement("tr");
      const aviso = document.createElement("td");
      aviso.colSpan = 5;
      aviso.textContent = "No hay pedidos.";
      fila.appendChild(aviso);
      pedidos.appendChild(fila);
      return;
    }

    lista.forEach((pedido) => {
      const fila = document.createElement("tr");
      fila.appendChild(celda(pedido.id));
      fila.appendChild(celda(pedido.cliente));
      fila.appendChild(celda(mostrarFecha(pedido.fecha)));
      fila.appendChild(celda(pedido.total));

      const estadoTd = document.createElement("td");
      const formulario = document.createElement("form");
      formulario.className = "fila";

      const select = document.createElement("select");
      estados.forEach((estado) => {
        const opcion = document.createElement("option");
        opcion.value = estado;
        opcion.textContent = estado;
        if (estado === pedido.estado) {
          opcion.selected = true;
        }
        select.appendChild(opcion);
      });
      formulario.appendChild(select);

      const boton = document.createElement("button");
      boton.type = "submit";
      boton.textContent = "Cambiar";
      formulario.appendChild(boton);

      const enlace = document.createElement("a");
      enlace.href = "pedido.html?id=" + pedido.id;
      enlace.textContent = "Ver";
      formulario.appendChild(enlace);

      formulario.addEventListener("submit", (evento) => {
        evento.preventDefault();
        pedir("/pedidos/" + pedido.id + "/estado", {
          method: "PUT",
          body: JSON.stringify({ estado: select.value }),
        })
          .then(() => {
            mensaje.textContent = "Estado actualizado";
            cargarPedidos();
          })
          .catch((error) => {
            mensaje.textContent = error.message;
          });
      });

      estadoTd.appendChild(formulario);
      fila.appendChild(estadoTd);
      pedidos.appendChild(fila);
    });
  });
}

if (!leerToken()) {
  mensaje.textContent = "Inicia sesión con la cuenta de administrador.";
  mostrarBloques(false);
} else {
  pedir("/auth/me")
    .then((usuario) => {
      if (usuario.rol !== "admin") {
        mensaje.textContent = "Esta página es solo para el administrador.";
        mostrarBloques(false);
        return;
      }

      cargarCategorias()
        .then(cargarProductos)
        .then(cargarPedidos)
        .catch((error) => {
          mensaje.textContent = error.message;
        });
    })
    .catch((error) => {
      mensaje.textContent = error.message;
    });
}

formCategoria.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const id = document.getElementById("categoria-id").value;
  const datos = {
    nombre: document.getElementById("categoria-nombre").value,
    descripcion: document.getElementById("categoria-descripcion").value,
  };

  let ruta = "/categorias/";
  let method = "POST";
  if (id) {
    ruta = "/categorias/" + id;
    method = "PUT";
  }

  pedir(ruta, { method: method, body: JSON.stringify(datos) })
    .then(() => {
      mensaje.textContent = id ? "Categoría actualizada" : "Categoría creada";
      formCategoria.reset();
      document.getElementById("categoria-id").value = "";
      cargarCategorias();
    })
    .catch((error) => {
      mensaje.textContent = error.message;
    });
});

document.getElementById("btn-cancelar-categoria").addEventListener("click", () => {
  formCategoria.reset();
  document.getElementById("categoria-id").value = "";
});

formProducto.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const id = document.getElementById("producto-id").value;
  const datos = {
    nombre: document.getElementById("producto-nombre").value,
    descripcion: document.getElementById("producto-descripcion").value,
    precio: Number(document.getElementById("producto-precio").value),
    stock: Number(document.getElementById("producto-stock").value),
    imagen: document.getElementById("producto-imagen").value,
    categoria_id: Number(document.getElementById("producto-categoria").value),
  };

  let ruta = "/productos/";
  let method = "POST";
  if (id) {
    ruta = "/productos/" + id;
    method = "PUT";
  }

  pedir(ruta, { method: method, body: JSON.stringify(datos) })
    .then(() => {
      mensaje.textContent = id ? "Producto actualizado" : "Producto creado";
      formProducto.reset();
      document.getElementById("producto-id").value = "";
      cargarProductos();
    })
    .catch((error) => {
      mensaje.textContent = error.message;
    });
});

document.getElementById("btn-cancelar-producto").addEventListener("click", () => {
  formProducto.reset();
  document.getElementById("producto-id").value = "";
});
