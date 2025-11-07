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

            fileDiv.addEventListener("click", () => {
            document.querySelectorAll(".file-grid-element.selected").forEach(el => el.classList.remove("selected"));
                showBottomMenu(file);
                fileDiv.classList.add("selected");
            });

            grid.appendChild(fileDiv);
        });
    } catch (error) {
        console.error("Błąd podczas ładowania plików:", error);
    }
}

// uruchamiamy funkcję po załadowaniu strony
document.addEventListener("DOMContentLoaded", loadFiles);

function showBottomMenu(filename) {
    const bottomMenu = document.getElementById("bottom-menu");
    bottomMenu.innerHTML = `
        <p>Selected file: ${filename}</p>
        <button id="analyze-btn">Analyze</button>
        <button id="delete-btn">Delete</button>
        <button id="close-btn">Close</button>
    `;
    bottomMenu.classList.remove("hidden");
    bottomMenu.classList.add("visible");
}