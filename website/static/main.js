document.addEventListener('DOMContentLoaded', async () => {
    const content = document.getElementById('content');
    const links = document.querySelectorAll('nav a');

    // Funkcja do obsługi formularzy
    function attachFormHandlers() {
        // Obsługa formularza ładowania plików
        const loadForm = document.getElementById('loadDataForm');
        if (loadForm) {
            loadForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(loadForm);
                const response = await fetch('/load_file', {
                    method: 'POST',
                    body: formData
                });
                if (response.redirected) {
                    // Jeśli serwer przekierował, załaduj nową stronę
                    const analyzeResponse = await fetch('/content/analyze');
                    const html = await analyzeResponse.text();
                    content.innerHTML = html;
                }
            });
        }

        // Obsługa formularza generowania sygnału
        const generateForm = document.getElementById('generateForm');
        if (generateForm) {
            generateForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(generateForm);
                try {
                    const response = await fetch('/generate_data', {
                        method: 'POST',
                        body: formData
                    });
                    if (response.ok) {
                        // Po udanym wygenerowaniu, przekieruj do analyze
                        const analyzeResponse = await fetch('/content/analyze');
                        const html = await analyzeResponse.text();
                        content.innerHTML = html;
                    } else {
                        alert('Wystąpił błąd podczas generowania sygnału');
                    }
                } catch (error) {
                    console.error('Błąd:', error);
                    alert('Wystąpił błąd podczas generowania sygnału');
                }
            });
        }
    }

    // Obsługa menu nawigacji
    links.forEach(link => {
        link.addEventListener('click', async () => {
            const page = link.dataset.page;
            const response = await fetch(`/content/${page}`);
            const html = await response.text();
            content.innerHTML = html;
            attachFormHandlers();
        });
    });

    // Załaduj analyze przy starcie
    const response = await fetch('/content/analyze');
    const html = await response.text();
    content.innerHTML = html;
    attachFormHandlers();
});