from flask import Blueprint, jsonify, request
import os
from werkzeug.utils import secure_filename

files_api = Blueprint("files_api", __name__)
UPLOAD_FOLDER = "app/uploads"

@files_api.route("/api/files/list")
def list_files():
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({
            "success": True,
            "files": files
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@files_api.route("/api/files/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({
                "success": False,
                "error": "No file part"
            }), 400

        file = request.files["file"]
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

        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        return jsonify({
            "success": True,
            "filename": filename
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500