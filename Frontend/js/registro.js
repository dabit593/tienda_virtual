const formulario = document.getElementById("form-registro");
const mensaje = document.getElementById("mensaje");

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const usuario = {
    nombre: document.getElementById("nombre").value,
    correo: document.getElementById("correo").value,
    password: document.getElementById("password").value,
  };

  pedir("/auth/register", {
    method: "POST",
    body: JSON.stringify(usuario),
  })
    .then(() => {
      mensaje.textContent = "Cuenta creada. Ahora inicia sesión.";
      formulario.reset();
    })
    .catch((error) => {
      mensaje.textContent = error.message;
    });
});
