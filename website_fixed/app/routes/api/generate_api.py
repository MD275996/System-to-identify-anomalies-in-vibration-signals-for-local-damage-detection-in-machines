from flask import Blueprint, request, jsonify
from app.services.file_service import save_file # tutaj będziemy musieli zaimportować inną funkcję, tę do generowania danych
from app.services.generate_service import gen_signal, save_to_file

generate_api = Blueprint('generate_api', __name__)

# jak dostaniemy post z js z formularzem do wygenerowania danych to powinnismy pobrać wszystkie zmienne, przesłać je do funckji z folderu services
# tam powinien się ten sygnał wygenerować i zapisać, a jak się skończy to dostaniemy odpowiedź że wszystko ok

@generate_api.post("/api/generate_data/generate")
def api_generate_data():
    try:
        # Pobierz i zwaliduj dane wejściowe
        field1 = request.form.get('field1')
        field2 = int(request.form.get('field2'))
        field3 = int(request.form.get('field3'))
        field4 = int(request.form.get('field4'))
        field5 = int(request.form.get('field5'))
        field6 = int(request.form.get('field6'))
        field7 = int(request.form.get('field7'))
        #field8 = int(request.form.get('field8'))

        # Generowanie sygnału
        try:
            signal = gen_signal(field2, field3, field4, field5, field6, field7)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error generating signal: {str(e)}"
            }), 500

        # Zapisywanie do pliku
        try:
            filename = f"{field1}.csv"
            save_to_file(signal, filename)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error saving file: {str(e)}"
            }), 500
        
        return jsonify({
            "success": True,
            "filename": filename
        })

    except (TypeError, ValueError) as e:
        return jsonify({
            "success": False,
            "error": f"Invalid input data: {str(e)}"
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500