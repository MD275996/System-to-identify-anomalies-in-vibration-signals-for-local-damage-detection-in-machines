from flask import Blueprint, request, jsonify
from app.services.file_service import save_file # tutaj będziemy musieli zaimportować inną funkcję, tę do generowania danych

generate_api = Blueprint('generate_api', __name__)

# jak dostaniemy post z js z formularzem do wygenerowania danych to powinnismy pobrać wszystkie zmienne, przesłać je do funckji z folderu services
# tam powinien się ten sygnał wygenerować i zapisać, a jak się skończy to dostaniemy odpowiedź że wszystko ok

@generate_api.post("/api/generate_data/generate")
def api_generate_data():
    try:
        field1 = int(request.form.get('field1'))
        field2 = int(request.form.get('field2'))
        field3 = int(request.form.get('field3'))
        field4 = int(request.form.get('field4'))
        field5 = int(request.form.get('field5'))
        field6 = int(request.form.get('field6'))
        field7 = int(request.form.get('field7'))
        
        return jsonify({"status":"ok"})
    except (TypeError, ValueError):
        return jsonify({"error":"Error: all fields must be integers!"}), 400