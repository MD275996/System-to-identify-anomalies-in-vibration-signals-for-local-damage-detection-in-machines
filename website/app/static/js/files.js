let currentFilename = null
let left = null
let right = null

async function loadFiles() {
    try {
        // wywołanie API
        const res = await fetch('/api/files/list');

        // odczytanie JSON
        const data = await res.json();
        const files = data.files;

        // pobieramy ul z HTML
        // const list = document.getElementById("file-list");
        const grid = document.querySelector(".file-grid");
        grid.innerHTML = "";
        
        //tworzymy grid plików i dodajemy event listenery
        files.forEach(file => {
            const fileDiv = document.createElement("div");
            fileDiv.className = "file-grid-element";
            fileDiv.textContent = file;

            fileDiv.addEventListener("click", () => {
            document.querySelectorAll(".file-grid-element.selected").forEach(el => el.classList.remove("selected"));
            fileDiv.classList.add("selected");
                const bottomMenu = document.getElementById("bottom-menu");
                document.getElementById("bottom-menu-filename").textContent = "Selected file: " + file;
                bottomMenu.classList.remove("hidden");
                bottomMenu.classList.add("visible");
                currentFilename = file;
            });

            grid.appendChild(fileDiv);
        });
    } catch (error) {
        console.error("Błąd podczas ładowania plików:", error);
    }
}

// uruchamiamy funkcję po załadowaniu strony
document.addEventListener("DOMContentLoaded", () =>{
    loadFiles();
    
    // obsługa przycisku show
    document.getElementById("show-btn").addEventListener("click", async () => {
        try{
            const res = await fetch(`/api/files/plot/${currentFilename}`);
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
    
    // zamykanie okienka wykresu
    document.getElementById("plot-close").addEventListener("click", () => {
        document.getElementById("plot-modal").classList.add("hidden");
    });

    // Obsługa przycisku Delete
    document.getElementById("delete-btn").addEventListener("click", async () => {
        try {
            const res = await fetch(`/api/files/delete/${currentFilename}`, {
                method: 'DELETE'
            });
            const response = await res.json();
            if (response.success) {
                // Odświeżenie listy plików
                await loadFiles();
                // Ukrycie menu dolnego
                const bottomMenu = document.getElementById("bottom-menu");
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

    // Obsługa przycisku Close
    document.getElementById("close-btn").addEventListener("click", () => {
        const bottomMenu = document.getElementById("bottom-menu");
        bottomMenu.classList.remove("visible");
        bottomMenu.classList.add("hidden");
        
        document.querySelectorAll(".file-grid-element.selected").forEach(el => el.classList.remove("selected"));
        
        const analyze_panel = document.getElementById("analyze_panel")
        const empty_right_panel = document.getElementById("empty_right_panel")
        analyze_panel.classList.add("hidden")
        empty_right_panel.classList.remove("hidden")
    });

    //obsługa przycisku Analyze
    document.getElementById("analyze-btn").addEventListener("click", async () => {
        if (!currentFilename) return;

        document.getElementById("filter-results").classList.add("hidden");
        document.getElementById("custom-boundaries-form").classList.add("hidden");
        document.getElementById("filter-boundaries-prompt").classList.remove("hidden");

        const analyzePanel = document.getElementById("analyze_panel");
        analyzePanel.classList.add("loading"); // panel wyszarzony i zablokowany

        try {
            // Wywołanie analizy pliku
            const res = await fetch(`/api/analyze/${currentFilename}`, { method: "POST" });
            const data = await res.json();

            if (!data.success) {
                alert("Analysis failed on server");
                return;
            }

            // Pobranie wyników analizy
            const resResult = await fetch("/api/analyze/result");
            const resultData = await resResult.json();

            if (!resultData.success) {
                document.getElementById("analyze-results").innerHTML = "<p>No data.</p>";
                return;
            }

            // Ustawienie nagłówka
            document.getElementById("analyze-results-filename").innerHTML = `
                <h2>Analysis shown for file: <b> ${currentFilename} </b></h2>
            `;

            // Pokazanie panelu
            const analyze_panel = document.getElementById("analyze_panel");
            const empty_right_panel = document.getElementById("empty_right_panel");
            analyze_panel.classList.remove("hidden");
            empty_right_panel.classList.add("hidden");

            // Czyszczenie kontenerów przed wstawieniem nowych wykresów
            const specContainer = document.getElementById("spectrogram-container");
            const selContainer = document.getElementById("selectors-container");
            specContainer.innerHTML = "";
            selContainer.innerHTML = "";

            // Wstawienie spektrogramu (pierwszy wykres)
            const specImg = document.createElement("img");
            specImg.src = resultData.plots[0] + "?t=" + Date.now();
            specImg.alt = "Spectrogram";
            specContainer.appendChild(specImg);

            // Wstawienie wykresów selektorów (pozostałe wykresy)
            resultData.plots.slice(1).forEach((path, i) => {
                const div = document.createElement("div");
                const title = document.createElement("h3");
                title.textContent = ["Spectral Kurtosis", "Jarque-Bera", "Kolmogorov-Smirnov", 
                                    "Anderson-Darling", "Cramer-von Mises", "Conditional Variance"][i] || `Selector ${i+1}`;
                const img = document.createElement("img");
                img.src = path + "?t=" + Date.now();
                img.alt = title.textContent;

                div.appendChild(title);
                div.appendChild(img);
                selContainer.appendChild(div);
            });

            // Ustawienie granic
            left = resultData.boundaries[0];
            right = resultData.boundaries[1];
            document.getElementById("boundaries-results").innerHTML = `
                <h3>IFB boundaries</h3>
                <span style="width: 100%; text-align: center;"><p>Detected IFB: [${left} - ${right}] Hz</p></span>
            `;

        } catch (err) {
            console.error(err);
            alert("Error during analysis. Check console.");
        } finally {
        analyzePanel.classList.remove("loading"); // odblokowanie panelu po zakończeniu
    }
    });

    //obsługa przycisku wyboru Select own boundaries
    document.getElementById("insert-boundaries-btn").addEventListener("click", () => {
        document.getElementById("custom-boundaries-form").classList.remove("hidden");
        document.getElementById("filter-boundaries-prompt").classList.add("hidden");
    });

    // Obsługa przycisku "Proceed"
    document.getElementById("proceed-btn").addEventListener("click", async () => {
        // API do analizy
        const res = await fetch("/api/analyze/filter", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                left: Number(left),
                right: Number(right)
            })
        });
        const result = await res.json();                
        //Wyniki po dokonanej filtracji
        if(result.success){
            const res = await fetch("/api/analyze/filter_results");
            const data = await res.json();
            document.getElementById("custom-boundaries-form").classList.add("hidden");
            document.getElementById("filter-boundaries-prompt").classList.add("hidden");
            document.getElementById("filter-results").classList.remove("hidden");
            document.getElementById(`filtered-signal`).src = data.plot + "?t=" + Date.now();
            document.getElementById(`result-message`).innerHTML = data.detection
            if (data.detection == "Impulse detected"){
                document.getElementById("result-message").style.color = "red"
            } else if(data.detection == "No impulse detected"){
                document.getElementById("result-message").style.color = "green"
            }
        } else {
            alert("Filtering failed.");
        }

    });

    //obsługa przycisku do wprowadzenia własnych granic
    document.getElementById("custom-boundaries-form").addEventListener("submit", async (e) => {
        e.preventDefault();

        left = Number(document.getElementById("lower-boundary").value);
        right = Number(document.getElementById("upper-boundary").value);

        if (!Number.isFinite(left) || !Number.isFinite(right)) {
            alert("Please enter valid numeric boundaries.");
            return;
        }

        if (left >= right) {
            alert("Lower boundary must be smaller than upper boundary.");
            return;
        }

        document.getElementById("boundaries-results").innerHTML = `
                <h3>IFB boundaries</h3>
                <span style="width: 100%; text-align: center;"><p>IFB: [${left} - ${right}] Hz</p></span>
            `;


        // API do analizy z własnymi granicami
        const res = await fetch("/api/analyze/filter", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                left: Number(left),
                right: Number(right)
            })
        });
        const result = await res.json();
        //Wyniki po dokonanej filtracji
        if(result.success){
            const res = await fetch("/api/analyze/filter_results");
            const data = await res.json();
            document.getElementById("custom-boundaries-form").classList.add("hidden");
            document.getElementById("filter-boundaries-prompt").classList.add("hidden");
            document.getElementById("filter-results").classList.remove("hidden");
            document.getElementById(`filtered-signal`).src = data.plot + "?t=" + Date.now();
            document.getElementById(`result-message`).innerHTML = data.detection
        } else {
            alert("Filtering failed.");
        }

    });
});
