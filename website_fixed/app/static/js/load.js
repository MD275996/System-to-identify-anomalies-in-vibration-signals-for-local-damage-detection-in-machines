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

        const response = await fetch("/api/files/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.status == "ok") {
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