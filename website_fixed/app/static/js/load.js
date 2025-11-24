// podpinamu się pod formularz upload-form i pod event "submit"
document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.preventDefault(); // zatrzymuje domyślne zachowanie formularza

    try {
        const file = document.getElementById("file-input").files[0];
        if (!file) {
            alert("Please select a file to upload.");
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
            alert("File uploaded successfully: " + data.filename);
            // Po udanym uploadzie, przekieruj do strony z plikami
            window.location.href = "/files";
        } else {
            alert("File upload failed: " + (data.error || "Unknown error"));
        }
    } catch (error) {
        console.error("Upload error:", error);
        alert("Error during file upload: " + error.message);
    }
});

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
    fileName.textContent = file.name;
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
            alert("Please select a file to upload.");
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
            alert("File uploaded successfully: " + data.filename);
            // Po udanym uploadzie, przekieruj do strony z plikami
            window.location.href = "/files";
        } else {
            alert("File upload failed: " + (data.error || "Unknown error"));
        }
    } catch (error) {
        console.error("Upload error:", error);
        alert("Error during file upload: " + error.message);
    }
  });
});