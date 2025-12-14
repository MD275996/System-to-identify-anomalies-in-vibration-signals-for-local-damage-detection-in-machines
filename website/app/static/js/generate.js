document.addEventListener('DOMContentLoaded', () => {
    const generateForm = document.getElementById("generateForm");

    const showGenerateModal = (message, redirectUrl = null) => {
        const modal = document.getElementById("generate-modal");
        const modalText = document.getElementById("generate-modal-text");
        const nextBtn = document.getElementById("generate-modal-next");

        modalText.textContent = message;
        modal.classList.remove("hidden");

        // usuwa poprzedni listener, żeby się nie nakładały
        nextBtn.replaceWith(nextBtn.cloneNode(true));
        const newNextBtn = document.getElementById("generate-modal-next");

        newNextBtn.addEventListener("click", () => {
            modal.classList.add("hidden");
            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        });
    };

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
                showGenerateModal("Signal generated successfully!", "/files");
            } else {
                showGenerateModal("Generation failed: " + (data.error || "Unknown error"));
            }
        } catch (error) {
            console.error("Generation error:", error);
            showGenerateModal("Error during signal generation: " + error.message);
        }
    });
});