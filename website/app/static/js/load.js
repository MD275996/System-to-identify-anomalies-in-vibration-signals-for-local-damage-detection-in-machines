// podpinamu się pod formularz upload-form i pod event "submit"
document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.preventDefault(); // zatrzymuje domyślne zachowanie formularza

    try {
        const file = document.getElementById("file-input").files[0];
        if (!file) {
            showModal("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/api/load/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showModal(`File loaded: ${data.filename}`, "/files");
        } else {
            showModal("File upload failed: " + (data.error || "Unknown error"));
        }
    } catch (error) {
    console.error("Upload error:", error);
    showModal("Error during file upload: " + error.message);
    } 
});

function showModal(message, redirectUrl = null) {
    const modal = document.getElementById("upload-modal");
    const modalText = document.getElementById("upload-modal-text");
    const nextBtn = document.getElementById("upload-modal-next");

    modalText.textContent = message;
    modal.classList.remove("hidden");

    // Usuń poprzedni listener, żeby nie nakładały się
    nextBtn.replaceWith(nextBtn.cloneNode(true));
    const newNextBtn = document.getElementById("upload-modal-next");

    newNextBtn.addEventListener("click", () => {
        modal.classList.add("hidden");
        console.log(1)
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const input = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const form = document.getElementById('upload-form');
    const progress = document.getElementById('progress');
    const progressBar = document.getElementById('progress-bar');
    const error = document.getElementById('error');

  const setFile = (file) => {
    if (!file) return;
    const preview = document.getElementById("file-preview");
    fileName.textContent = file.name;
    fileName.classList.add("visible");
    preview.classList.remove("hidden"); // pokaż ikonę i nazwę
    error.hidden = true;
  };

  dropzone.addEventListener('click', () => input.click());
  dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    const f = e.dataTransfer.files[0];
    input.files = e.dataTransfer.files;
    setFile(f);
  });

  input.addEventListener('change', () => setFile(input.files[0]));

  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    try {
        const file = document.getElementById("file-input").files[0];
        if (!file) {
            showModal("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/api/load/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            // ustaw nazwę pliku w modal
            const modal = document.getElementById("upload-modal");
            const modalText = document.getElementById("upload-modal-text");
            modalText.textContent = `File loaded: ${data.filename}`;
            modal.classList.remove("hidden"); // pokaż modal

            // obsługa przycisku "Dalej"
            document.getElementById("upload-modal-next").addEventListener("click", () => {
                modal.classList.add("hidden"); // zamknij modal
                window.location.href = "/files"; // przekieruj
            }); 
        } else {
            showModal("File upload failed: " + (data.error || "Unknown error"));
            }
    } catch (error) {
    console.error("Upload error:", error);
    showModal("Error during file upload: " + error.message);
    }
  });
});