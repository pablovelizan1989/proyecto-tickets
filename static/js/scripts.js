// Validación Bootstrap
(() => {
  'use strict';
  const forms = document.querySelectorAll('.needs-validation');

  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        alert("Por favor, completá todos los campos obligatorios correctamente.");
      } else {
        alert("La compra se realizó correctamente ✔️");
      }
      form.classList.add('was-validated');
    }, false);
  });
})();
