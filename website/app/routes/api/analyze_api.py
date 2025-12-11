from flask import Blueprint, request, jsonify, session
from app.services.analyze_service import process_file

analyze_api = Blueprint('analyze_api', __name__)

#tworzy blueprin o nazwie files_api, mini-aplikacja Flaska, którą potem włączę w główną aplikację
# pozwala mieć strunkturę /api/files/* lub /api/data/* itp

@analyze_api.post("/api/analyze/<filename>")                           

def api_analyze_file(filename):
    try:
        output_paths, boundaries = process_file(filename)

        session["analyze_results"] = {
            "filename": filename,
            "plots":output_paths,
            "boundaries": boundaries
        }

        return jsonify({"success":True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@analyze_api.get("/api/analyze/result")
def api_analyze_result():
    result = session.get("analyze_results")
    if not result:
        return jsonify({"success": False, "error": "No analysis done"}), 404
    return jsonify({
        "success":True,
        "filename": result["filename"],
        "plots": result["plots"],
        "boundaries": result["boundaries"],
    })
