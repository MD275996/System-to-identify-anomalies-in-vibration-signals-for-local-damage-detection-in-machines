// podpinamu się pod formularz upload-form i pod event "submit"
document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.precentDefault(); // zatrzymuje domyślne zachowanie formularza

    const file = document.getElementById("file-input").files[0];    //pobieramy plik z inputa
    if (!file){ //sprawdzenie czy plik dodano
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();    //tworzymy FormData czyli specjalny obiekt w js który potrafi przenosić pliki i takie tam rzeczy 
    formData.append("file", file);

    // wysyłamy fetch do API, czyli post na adres api/files/upload i czekamy na odpowiedź
    const res = await fetch("/api/files/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    // potwierdzenie czy akcja się udała czy nie
    if (data.status === "ok"){
        alert("File uploaded successfully: " + data.filename);
    }else{
        alert("File upload failed: ");
    }
});