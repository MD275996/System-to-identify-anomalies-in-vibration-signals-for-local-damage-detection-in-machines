document.addEventListener('DOMContentLoaded', async () => {
    // Obsługa linków w menu z data-page (tylko dla load, generate, info)
    const links = document.querySelectorAll('nav a[data-page]');
    
    async function loadPage(page) {
        try {
            const response = await fetch(`/content/${page}`);
            const html = await response.text();
            document.getElementById('content').innerHTML = html;
        } catch (error) {
            console.error(`Błąd podczas ładowania strony ${page}:`, error);
        }
    }

    // Dodaj obsługę kliknięć dla linków z data-page
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            loadPage(page);
        });
    });
});