const lista = document.getElementById("lista");
const mensaje = document.getElementById("mensaje");

function celda(texto) {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function pintarPedidos(pedidos) {
  vaciar(lista);

  if (pedidos.length === 0) {
    const fila = document.createElement("tr");
    const aviso = document.createElement("td");
    aviso.colSpan = 5;
    aviso.textContent = "Todavía no tienes pedidos.";
    fila.appendChild(aviso);
    lista.appendChild(fila);
    return;
  }

  pedidos.forEach((pedido) => {
    const fila = document.createElement("tr");
    fila.appendChild(celda(pedido.id));
    fila.appendChild(celda(mostrarFecha(pedido.fecha)));
    fila.appendChild(celda(pedido.estado));
    fila.appendChild(celda(dinero(pedido.total)));

    const acciones = document.createElement("td");
    const enlace = document.createElement("a");
    enlace.href = "pedido.html?id=" + pedido.id;
    enlace.textContent = "Ver detalle";
    acciones.appendChild(enlace);
    fila.appendChild(acciones);

    lista.appendChild(fila);
  });
}

if (!leerToken()) {
  mensaje.textContent = "Inicia sesión para ver tus pedidos.";
} else {
  pedir("/pedidos/mios")
    .then(pintarPedidos)
    .catch((error) => {
      mensaje.textContent = error.message;
    });
}
