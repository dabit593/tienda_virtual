const destacados = document.getElementById("destacados");
const categorias = document.getElementById("categorias");

pedir("/productos/aleatorios?cantidad=4")
  .then((productos) => {
    pintarProductos(destacados, productos, "Todavía no hay productos.");
  })
  .catch((error) => {
    destacados.textContent = error.message;
  });

pedir("/categorias")
  .then((lista) => {
    vaciar(categorias);

    const menu = document.createElement("ul");

    lista.forEach((categoria) => {
      const item = document.createElement("li");
      const enlace = document.createElement("a");
      enlace.href = "catalogo.html?categoria=" + categoria.id;
      enlace.textContent = categoria.nombre;
      item.appendChild(enlace);
      menu.appendChild(item);
    });

    categorias.appendChild(menu);
  })
  .catch((error) => {
    categorias.textContent = error.message;
  });
