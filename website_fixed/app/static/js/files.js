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
        <button id="show-btn">Show</button>
        <button id="delete-btn">Delete</button>
        <button id="close-btn">Close</button>`;
    bottomMenu.classList.remove("hidden");
    bottomMenu.classList.add("visible");

    // obsługa przycisku show
    document.getElementById("show-btn").addEventListener("click", async () => {
        try{
            const res = await fetch(`/api/files/plot/${filename}`);
            const data = await res.json();

            if(!data.success){
                alert("Plot generation failed!");
                return;
            }

            console.log(1)
            // ustaw obraze w modalu
            const img = document.getElementById("plot-image");
            img.src = data.url;

            //pokaz modal
            document.getElementById("plot-modal").classList.remove("hidden");
        }catch(err){
            console.error(err);
            alert("Error generating plot",err);
        }
    });
    //zamykanie modalu
    document.getElementById("plot-close").addEventListener("click", () => {
        document.getElementById("plot-modal").classList.add("hidden");
    });


    // Obsługa przycisku Delete
    document.getElementById("delete-btn").addEventListener("click", async () => {
        try {
            const res = await fetch(`/api/files/delete/${filename}`, {
                method: 'DELETE'
            });
            const response = await res.json();
            if (response.success) {
                // Odświeżenie listy plików
                await loadFiles();
                // Ukrycie menu dolnego
                bottomMenu.classList.remove("visible");
                bottomMenu.classList.add("hidden");
            } else {
                const errorData = await response.json();
                alert(`Error deleting file: ${errorData.message || 'Unknown error'}`);
            }
        } catch (error) {
            console.error("Error during file deletion:", error);
            alert("Failed to delete file. Please try again.");
        }
    });

    //obsługa przycisku Analyze
    document.getElementById("analyze-btn").addEventListener("click", async () => {
        const res = await fetch(`/api/analyze/${filename}`, {
            method: "POST"
        });
        const data = await res.json();

        console.log("Sending analysis request for:", filename);
        console.log("Response:", data); 

        if (data.success) {
            window.location.href = "/analyze";
        } else {
            alert("Analysis failed");
        }
    });

    // Obsługa przycisku Close
    document.getElementById("close-btn").addEventListener("click", () => {
        bottomMenu.classList.remove("visible");
        bottomMenu.classList.add("hidden");
        document.querySelectorAll(".file-grid-element.selected").forEach(el => el.classList.remove("selected"));
    });
}