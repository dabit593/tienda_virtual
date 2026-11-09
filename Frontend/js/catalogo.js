const lista = document.getElementById("lista");
const mensaje = document.getElementById("mensaje");
const formulario = document.getElementById("form-buscar");
const campoTexto = document.getElementById("texto");
const campoCategoria = document.getElementById("categoria");
const params = new URLSearchParams(window.location.search);

campoTexto.value = params.get("q") || "";

function cargarProductos() {
  const texto = campoTexto.value.trim();
  const categoria = campoCategoria.value;
  let ruta = "/productos/buscar?";

  if (texto) {
    ruta = ruta + "texto=" + encodeURIComponent(texto) + "&";
  }

  if (categoria) {
    ruta = ruta + "categoria_id=" + categoria;
  }

  pedir(ruta)
    .then((productos) => {
      mensaje.textContent = "";
      pintarProductos(lista, productos, "No hay productos con esa búsqueda.");
    })
    .catch((error) => {
      mensaje.textContent = error.message;
    });
}

pedir("/categorias")
  .then((categorias) => {
    categorias.forEach((categoria) => {
      const opcion = document.createElement("option");
      opcion.value = categoria.id;
      opcion.textContent = categoria.nombre;
      campoCategoria.appendChild(opcion);
    });

    const categoriaInicial = params.get("categoria");
    if (categoriaInicial) {
      campoCategoria.value = categoriaInicial;
    }

    cargarProductos();
  })
  .catch((error) => {
    mensaje.textContent = error.message;
  });

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();
  cargarProductos();
});
