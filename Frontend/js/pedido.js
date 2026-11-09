const ficha = document.getElementById("ficha");
const mensaje = document.getElementById("mensaje");
const params = new URLSearchParams(window.location.search);
const id = params.get("id");

function celda(texto) {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function pintarPedido(pedido) {
  vaciar(ficha);

  const titulo = document.createElement("h1");
  titulo.textContent = "Pedido " + pedido.id;
  ficha.appendChild(titulo);

  const fecha = document.createElement("p");
  fecha.textContent = mostrarFecha(pedido.fecha);
  ficha.appendChild(fecha);

  const estado = document.createElement("p");
  estado.textContent = "Estado: " + pedido.estado;
  ficha.appendChild(estado);

  const cliente = document.createElement("p");
  cliente.textContent = "Cliente: " + pedido.cliente;
  ficha.appendChild(cliente);

  const tabla = document.createElement("table");
  tabla.border = "1";

  const cabeza = document.createElement("thead");
  const encabezado = document.createElement("tr");
  ["Producto", "Cantidad", "Precio", "Subtotal"].forEach((nombre) => {
    const th = document.createElement("th");
    th.textContent = nombre;
    encabezado.appendChild(th);
  });
  cabeza.appendChild(encabezado);
  tabla.appendChild(cabeza);

  const cuerpo = document.createElement("tbody");
  pedido.items.forEach((item) => {
    const fila = document.createElement("tr");
    fila.appendChild(celda(item.nombre));
    fila.appendChild(celda(item.cantidad));
    fila.appendChild(celda(dinero(item.precio_unitario)));
    fila.appendChild(celda(dinero(item.subtotal)));
    cuerpo.appendChild(fila);
  });
  tabla.appendChild(cuerpo);
  ficha.appendChild(tabla);

  const total = document.createElement("p");
  total.textContent = "Total: " + dinero(pedido.total);
  ficha.appendChild(total);
}

if (!leerToken()) {
  ficha.textContent = "Inicia sesión para ver el pedido.";
} else if (!id) {
  ficha.textContent = "No se indicó el pedido.";
} else {
  pedir("/pedidos/" + id)
    .then(pintarPedido)
    .catch((error) => {
      mensaje.textContent = error.message;
    });
}
