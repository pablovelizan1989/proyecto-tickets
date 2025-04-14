function calcTotal() {
    const precioBase = 10000;
    const cant = parseInt(document.getElementById("cant").value);
    const categoria = document.getElementById("desc").value;

    const descuentos = {
        estudiante: 0.50,
        profesional: 0.30,
        orador: 0.10
    };

    if (!cant || cant <= 0) {
        document.getElementById("total").innerHTML = "⚠️ Ingresá una cantidad válida";
        document.getElementById("total").className = "bg-danger p-2 text-white";
        return;
    }

    const descuento = descuentos[categoria] || 0;
    const total = precioBase * cant * (1 - descuento);

    document.getElementById("total").innerHTML = `$${total.toLocaleString('es-AR')}`;
    document.getElementById("total").className = "bg-info p-2 text-dark";

    // Precios con descuento para cada categoría
    document.getElementById("precio-estudiante").textContent =
        `$${(precioBase * cant * (1 - descuentos.estudiante)).toLocaleString('es-AR')}`;
    document.getElementById("precio-profesional").textContent =
        `$${(precioBase * cant * (1 - descuentos.profesional)).toLocaleString('es-AR')}`;
    document.getElementById("precio-orador").textContent =
        `$${(precioBase * cant * (1 - descuentos.orador)).toLocaleString('es-AR')}`;
}

function seleccionarCategoria(categoria) {
    document.getElementById("desc").value = categoria;

    const campoCantidad = document.getElementById("cant");

    if (!campoCantidad.value || parseInt(campoCantidad.value) === 0) {
        campoCantidad.value = 1;  // 👉 asigna 1 si está vacío o en 0
    }

    calcTotal();
}

// ✅ Esperar al DOM antes de registrar el evento submit
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-tickets');

    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');

            // ⚠️ Elimina el alert para que Flask pueda procesar
            // alert("Por favor, completá todos los campos obligatorios correctamente.");
        }
    });
});
