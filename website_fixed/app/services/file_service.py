import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "app/uploads"

def save_file(file):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename

def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return files

def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False