const ficha = document.getElementById("ficha");
const mensaje = document.getElementById("mensaje");
const params = new URLSearchParams(window.location.search);
const id = params.get("id");

if (!id) {
  ficha.textContent = "No se indicó el producto.";
} else {
  pedir("/productos/" + id)
    .then((producto) => {
      vaciar(ficha);

      const imagen = document.createElement("img");
      imagen.src = urlImagen(producto.imagen);
      imagen.alt = producto.nombre;
      imagen.className = "figura_producto";
      ficha.appendChild(imagen);

      const datos = document.createElement("div");

      const titulo = document.createElement("h1");
      titulo.textContent = producto.nombre;
      datos.appendChild(titulo);

      const categoria = document.createElement("p");
      categoria.textContent = "Categoría: " + producto.categoria;
      datos.appendChild(categoria);

      const precio = document.createElement("p");
      precio.className = "precio";
      precio.textContent = dinero(producto.precio);
      datos.appendChild(precio);

      const descripcion = document.createElement("p");
      descripcion.textContent = producto.descripcion;
      datos.appendChild(descripcion);

      const stock = document.createElement("p");
      stock.textContent = "Stock: " + producto.stock;
      datos.appendChild(stock);

      if (producto.stock > 0) {
        const formulario = document.createElement("form");
        formulario.className = "fila";

        const cantidad = document.createElement("input");
        cantidad.type = "number";
        cantidad.min = "1";
        cantidad.max = String(producto.stock);
        cantidad.value = "1";
        formulario.appendChild(cantidad);

        const boton = document.createElement("button");
        boton.type = "submit";
        boton.textContent = "Agregar al carrito";
        formulario.appendChild(boton);

        formulario.addEventListener("submit", (evento) => {
          evento.preventDefault();

          if (!leerToken()) {
            mensaje.textContent = "Inicia sesión para agregar al carrito.";
            return;
          }

          const pedida = Number(cantidad.value);
          if (pedida < 1 || pedida > producto.stock) {
            mensaje.textContent = "Revisa la cantidad. Hay " + producto.stock + " disponibles.";
            return;
          }

          pedir("/carrito/items", {
            method: "POST",
            body: JSON.stringify({
              producto_id: producto.id,
              cantidad: pedida,
            }),
          })
            .then(() => {
              mensaje.textContent = "Producto agregado al carrito.";
            })
            .catch((error) => {
              mensaje.textContent = error.message;
            });
        });

        datos.appendChild(formulario);
      } else {
        const aviso = document.createElement("p");
        aviso.textContent = "Este producto no tiene stock.";
        datos.appendChild(aviso);
      }

      ficha.appendChild(datos);
    })
    .catch((error) => {
      ficha.textContent = error.message;
    });
}
