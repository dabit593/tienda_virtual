const lista = document.getElementById("lista");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");
const comprar = document.getElementById("btn-comprar");

function celda(texto) {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function pintarCarrito(carrito) {
  vaciar(lista);
  total.textContent = "Total: " + dinero(carrito.total);

  if (carrito.items.length === 0) {
    const fila = document.createElement("tr");
    const aviso = document.createElement("td");
    aviso.colSpan = 5;
    aviso.textContent = "El carrito está vacío.";
    fila.appendChild(aviso);
    lista.appendChild(fila);
    comprar.hidden = true;
    return;
  }

  comprar.hidden = false;

  carrito.items.forEach((item) => {
    const fila = document.createElement("tr");
    fila.appendChild(celda(item.nombre));
    fila.appendChild(celda(dinero(item.precio)));

    const cantidadTd = document.createElement("td");
    const formulario = document.createElement("form");
    formulario.className = "fila";

    const cantidad = document.createElement("input");
    cantidad.type = "number";
    cantidad.min = "1";
    cantidad.max = String(item.stock);
    cantidad.value = String(item.cantidad);
    formulario.appendChild(cantidad);

    const actualizar = document.createElement("button");
    actualizar.type = "submit";
    actualizar.textContent = "Actualizar";
    formulario.appendChild(actualizar);

    formulario.addEventListener("submit", (evento) => {
      evento.preventDefault();
      pedir("/carrito/items/" + item.id, {
        method: "PUT",
        body: JSON.stringify({ cantidad: Number(cantidad.value) }),
      })
        .then(pintarCarrito)
        .catch((error) => {
          mensaje.textContent = error.message;
        });
    });

    cantidadTd.appendChild(formulario);
    fila.appendChild(cantidadTd);
    fila.appendChild(celda(dinero(item.subtotal)));

    const acciones = document.createElement("td");
    const quitar = document.createElement("button");
    quitar.type = "button";
    quitar.textContent = "Quitar";
    quitar.addEventListener("click", () => {
      pedir("/carrito/items/" + item.id, { method: "DELETE" })
        .then(pintarCarrito)
        .catch((error) => {
          mensaje.textContent = error.message;
        });
    });
    acciones.appendChild(quitar);
    fila.appendChild(acciones);

    lista.appendChild(fila);
  });
}

if (!leerToken()) {
  mensaje.textContent = "Inicia sesión para ver el carrito.";
  comprar.hidden = true;
} else {
  pedir("/carrito/")
    .then(pintarCarrito)
    .catch((error) => {
      mensaje.textContent = error.message;
    });

  comprar.addEventListener("click", () => {
    pedir("/pedidos/", { method: "POST" })
      .then((pedido) => {
        window.location.href = "pedido.html?id=" + pedido.id;
      })
      .catch((error) => {
        mensaje.textContent = error.message;
      });
  });
}
