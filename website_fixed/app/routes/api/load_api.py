from flask import Blueprint, request, jsonify
from app.services.file_service import save_file                 #własna funkcja z warstwy services, sluży do zapisu pliku

load_api = Blueprint('load_api', __name__)

#tworzy blueprin o nazwie files_api, mini-aplikacja Flaska, którą potem włączę w główną aplikację
# pozwala mieć strunkturę /api/files/* lub /api/data/* itp

@load_api.post("/api/load/upload")                            #dekorator, uruchamia tę funkcję przy żądaniu POST pod adresem /api/files/upload

#adres /api/files/upload jest wywoływany przez fetch w pliku js, tam go znajdę
def api_upload_file():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No file part"
        }), 400
    file = request.files.get("file")                            #pobiera plik z żądania HTTP

    #niżej sprawdzamy czy plik istnieje i zwracamy odpowiedź JSON

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "No selected file"
        }), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({
            "success": False,
            "error": "Only CSV files are allowed"
        }), 400

    filename = save_file(file)
    
    return jsonify({"success":True,"filename": filename})