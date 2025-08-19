// main.js - Se cargará en todas las páginas

document.addEventListener("DOMContentLoaded", () => {
    // Saludo dinámico segun la hora
    const saludoEl = document.querySelector("#saludo-dinamico");
    if (saludoEl) {
        const hora = new Date().getHours();
        let saludo;
        if (hora < 12) saludo = "☀️ Buenos días";
        else if (hora < 19) saludo = "🌤️ Buenas tardes";
        else saludo = "🌙 Buenas noches";
        saludoEl.textContent = `${saludo}, ${saludoEl.dataset.username || "usuario"}`;
    }

    // Animación para contadores del dashboard
    document.querySelectorAll(".stat-number[data-count]").forEach(el => {
        let target = parseInt(el.dataset.count, 10);
        let current = 0;
        let increment = Math.ceil(target / 50);

        const counter = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(counter);
            }
            el.textContent = current;
        }, 30);
    });
});
