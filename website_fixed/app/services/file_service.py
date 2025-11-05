import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "app/uploads"

def save_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename