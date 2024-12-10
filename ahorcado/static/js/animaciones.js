document.addEventListener('DOMContentLoaded', function () {
    const mensajeAnimado = document.getElementById('mensaje-animado');
    mensajeAnimado.style.display = 'block';

    // Opcional: Ocultar animación después de 5 segundos
    setTimeout(() => {
        mensajeAnimado.style.display = 'block';
    }, 10 * 1000);
});


