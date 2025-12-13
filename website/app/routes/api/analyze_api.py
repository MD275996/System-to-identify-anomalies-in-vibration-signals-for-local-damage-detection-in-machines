from flask import Blueprint, request, jsonify, session
from app.services.analyze_service import process_file
from app.services.analyze_service import bandpass_filter
from app.services.analyze_service import impuls_detection
from app.services.analyze_service import get_signal_from_file
from app.services.analyze_service import draw_signal

analyze_api = Blueprint('analyze_api', __name__)

#tworzy blueprin o nazwie files_api, mini-aplikacja Flaska, którą potem włączę w główną aplikację
# pozwala mieć strunkturę /api/files/* lub /api/data/* itp



@analyze_api.post("/api/analyze/<filename>")                           
def api_analyze_file(filename):
    try:
        signal = get_signal_from_file(filename)
        output_paths, boundaries = process_file(signal)

        session["filename"] = filename
        session["plots"]=output_paths
        session["boundaries"]=boundaries

        return jsonify({"success":True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@analyze_api.post("/api/analyze/filter")                           
def api_analize_filter():
    try:
        if "filename" not in session:
            return jsonify({
                "success": False,
                "error": "No analysis context"
            }),400
        data = request.get_json()

        lower = data.get("left")
        upper = data.get("right")

        if lower is None or upper is None:
            return jsonify({
                "success": False,
                "error": "Missing boundaries"
            }), 400

        signal = get_signal_from_file(session.get("filename"))
        filtered,_,_,_ =bandpass_filter(signal, len(signal), lower, upper)
        
        plot_path = draw_signal(filtered, "filtered_"+session.get("filename"))
        session["filtered_signal"] = plot_path

        result = impuls_detection(filtered)
        if result > 0.025:
            session["detection"]="Impulse detected"
        else:
            session["detection"]="No impulse detected"

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }),500
    
@analyze_api.get("/api/analyze/result")
def api_analyze_result():

    filename = session.get("filename")
    plots = session.get("plots")    
    boundaries = session.get("boundaries")
    if not filename:
        return jsonify({"success": False, "error": "No analysis done"}), 404
    return jsonify({
        "success":True,
        "filename": filename,
        "plots": plots,
        "boundaries": boundaries,
    })

@analyze_api.get("/api/analyze/filter_results")    
def api_analyze_filter_result():
    detection = session.get("detection")
    plot_path = session.get("filtered_signal")

    if not detection or not plot_path:
        return jsonify({
            "success": False,
            "error": "Filtration failed"
            }), 404
    return jsonify({
        "success":True,
        "detection": detection,
        "plot": plot_path
    }) 