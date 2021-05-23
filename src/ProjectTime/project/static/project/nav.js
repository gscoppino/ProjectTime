document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.navbar-burger');
    if (nav === null) {
        return;
    }

    nav.addEventListener('click', () => {
        const target = document.getElementById(nav.dataset.target);
        nav.classList.toggle('is-active');
        target.classList.toggle('is-active');
    });
});
