document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
        row.style.opacity = 0;
        setTimeout(() => {
            row.style.opacity = 1;
            row.style.transform = 'translateY(0)';
            row.style.transition = 'all 0.7s ease';
        }, index * 300); // Retardo para cada fila
    });
});