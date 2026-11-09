const formulario = document.getElementById("form-login");
const mensaje = document.getElementById("mensaje");

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const datos = new URLSearchParams();
  datos.append("username", document.getElementById("correo").value);
  datos.append("password", document.getElementById("password").value);

  pedir("/auth/login", {
    method: "POST",
    body: datos,
  })
    .then((respuesta) => {
      localStorage.setItem("token", respuesta.access_token);
      window.location.href = "index.html";
    })
    .catch((error) => {
      mensaje.textContent = error.message;
    });
});
