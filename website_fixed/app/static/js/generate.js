document.addEventListener('DOMContentLoaded', () => {
    const generateForm = document.getElementById("generateForm");
    

    generateForm.addEventListener("submit", async function(e) {
        e.preventDefault();

        try {
            const formData = new FormData(e.target);

            const response = await fetch("/api/generate_data/generate", {
                method: "POST",
                body: formData
            });


            const data = await response.json();

            if (data.success) {
                alert("Signal generated successfully!");
                // Po wygenerowaniu, przekieruj do strony z plikami
                window.location.href = "/files";
            } else {
                alert("Generation failed: " + (data.error || "Unknown error"));
            }
        } catch (error) {
            console.error("Generation error:", error);
            alert("Error during signal generation: " + error.message);
        }
    });
});
