import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

def save_file(file):
    if file and "." in file.filename:
        ext = file.filename.rsplit(".",1)[1].lower()
        if ext in ALLOWED_EXT:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            return filename
    return ""
