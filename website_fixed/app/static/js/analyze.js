async function loadPlots() {
    const res = await fetch("/api/analyze/result");
    const data = await res.json();

    if (!data.success){
        document.getElementById("plots").innerHTML = "<p> No data.</p>"
        return;
    }
    const container = document.getElementById("plots");

    data.plots.forEach(path => {
        const img = document.createElement("img")
        img.src = path;
        img.style.width = "400px";
        img.style.margin = "10px";
        container.appendChild(img);        
    });
}
loadPlots();