const API = "http://127.0.0.1:8000";

function leerToken() {
  return localStorage.getItem("token");
}

function pedir(ruta, opciones) {
  const config = opciones || {};
  const headers = new Headers(config.headers || {});
  const token = leerToken();

  if (token) {
    headers.set("Authorization", "Bearer " + token);
  }

  if (config.body && !(config.body instanceof URLSearchParams)) {
    headers.set("Content-Type", "application/json");
  }

  return fetch(API + ruta, {
    method: config.method || "GET",
    headers: headers,
    body: config.body || null,
  }).then((response) => {
    return response.json().then((datos) => {
      if (!response.ok) {
        let texto = "No se pudo completar la acción";
        if (typeof datos.detail === "string") {
          texto = datos.detail;
        }
        throw new Error(texto);
      }
      return datos;
    });
  });
}

function urlImagen(ruta) {
  if (!ruta) {
    return "";
  }
  if (ruta.startsWith("http")) {
    return ruta;
  }
  return API + ruta;
}

function dinero(valor) {
  return "$" + Number(valor).toFixed(2);
}

function vaciar(elemento) {
  while (elemento.firstChild) {
    elemento.removeChild(elemento.firstChild);
  }
}

function mostrarFecha(fecha) {
  const valor = new Date(fecha);
  return valor.toLocaleString();
}
