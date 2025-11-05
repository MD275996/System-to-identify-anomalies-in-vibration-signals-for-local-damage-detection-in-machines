from flask import Blueprint, request, jsonify
from app.services.file_service import save_file #własna funkcja z warstwy services, sluży do zapisu pliku

files_api = Blueprint('files_api', __name__)
#tworzy blueprin o nazwie files_api, mini-aplikacja Flaska, którą potem włączę w główną aplikację
# pozwala mieć strunkturę /api/files/* lub /api/data/* itp

@files_api.post("/api/files/upload") #dekorator, uruchamia tę funkcję przy żądaniu POST pod adresem /api/files/upload
# adres /api/files/upload jest wywoływany przez fetch w pliku js, tam go znajdę
def api_upload_file():
    file = request.files.get("file") #pobiera plik z żądania HTTP
    #niżej sprawdzamy czy plik istnieje i zwracamy odpowiedź JSON
    if not file:
        return jsonify({"error": "No file provided"}), 400
    filename = save_file(file)
    return jsonify({"status":"ok","filename": filename})
