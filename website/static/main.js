document.addEventListener('DOMContentLoaded', async () => {
    const content = document.getElementById('content');
    const links = document.querySelectorAll('nav a');

    links.forEach(link => {
        link.addEventListener('click', async () => {
            const page = link.dataset.page;
            const response = await fetch(`/content/${page}`);
            const html = await response.text();
            content.innerHTML = html;
            attachFormHandler();
        });
    });

    // Funkcja do obsługi formularza
    function attachFormHandler() {
        const form = document.getElementById('loadDataForm');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // nie przeładowuj strony
            const formData = new FormData(form);

            const response = await fetch('/load_file', {
                method: 'POST',
                body: formData
            });

            const html = await response.text();
            document.getElementById('content').innerHTML = html;    // podmień treść
        });
    }

    // Załaduj analyze przy starcie
    const response = await fetch('/content/analyze');
    const html = await response.text();
    content.innerHTML = html;
    attachFormHandler();
});