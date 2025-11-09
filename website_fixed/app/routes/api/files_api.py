from flask import Blueprint, request, jsonify
from app.services.file_service import save_file                 #własna funkcja z warstwy services, sluży do zapisu pliku

files_api = Blueprint('files_api', __name__)

#tworzy blueprin o nazwie files_api, mini-aplikacja Flaska, którą potem włączę w główną aplikację
# pozwala mieć strunkturę /api/files/* lub /api/data/* itp

@files_api.post("/api/files/upload")                            #dekorator, uruchamia tę funkcję przy żądaniu POST pod adresem /api/files/upload

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

@files_api.get("/api/files/list")
def api_list_files():
    from app.services.file_service import list_files
    files = list_files()
    return jsonify({"files": files})

@files_api.delete("/api/files/delete/<filename>")
def api_delete_file(filename):
    from app.services.file_service import delete_file
    success = delete_file(filename)
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "File not found"}), 404
