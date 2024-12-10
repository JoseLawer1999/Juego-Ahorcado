document.addEventListener('DOMContentLoaded', function () {
    const nav = document.getElementById('navegacion');
    nav.style.opacity = 0;
    setTimeout(() => {
        nav.style.opacity = 1;
        nav.style.transition = 'opacity 2.5s';
    }, 100);
});

/*
document.addEventListener("DOMContentLoaded", function () {
    const timerElement = document.getElementById("timer");
    let seconds = 60;

    function updateTimer() {
        seconds--;
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    }

    setInterval(updateTimer, 1000);
});
*/



