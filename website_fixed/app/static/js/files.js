async function loadFiles() {
    try {
        // wywołanie API
        const res = await fetch('/api/files/list');

        // odczytanie JSON
        const data = await res.json();
        const files = data.files;

        //pobieramy ul z HTML
        // const list = document.getElementById("file-list");
        const grid = document.querySelector(".file-grid");
        grid.innerHTML = "";

        files.forEach(file => {
            const fileDiv = document.createElement("div");
            fileDiv.className = "file-grid-element";
            fileDiv.textContent = file;
            grid.appendChild(fileDiv);
        });
    } catch (error) {
        console.error("Błąd podczas ładowania plików:", error);
    }
}

// uruchamiamy funkcję po załadowaniu strony
document.addEventListener("DOMContentLoaded", loadFiles);