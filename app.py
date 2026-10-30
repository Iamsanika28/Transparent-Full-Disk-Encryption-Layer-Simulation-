from pathlib import Path

from flask import Flask, request, render_template, render_template_string, redirect, url_for
from werkzeug.exceptions import RequestEntityTooLarge
from encryption_layer import TransparentEncryptionLayer

BASE_DIR = Path(__file__).resolve().parent
DECRYPTED_DIR = BASE_DIR / "decrypted"
DECRYPTED_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

disk = TransparentEncryptionLayer()

RESULT_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SecureDisk Result</title>
<style>
body{font-family:Arial;background:#0f172a;color:#e2e8f0;
padding:40px 16px;text-align:center}
.card{max-width:600px;margin:auto;background:#1e293b;
padding:28px;border-radius:14px;overflow-wrap:anywhere}
a{color:#67e8f9}
</style>
</head>
<body>
<div class="card">
<h1>SecureDisk</h1>
<p>{{ message }}</p>
<p><a href="/">Return to the main page</a></p>
</div>
</body>
</html>
"""

def result(message):
    return render_template_string(RESULT_PAGE, message=message)

def valid_filename(filename):
    return (
        bool(filename)
        and filename not in {".", ".."}
        and Path(filename).name == filename
        and "/" not in filename
        and "\\" not in filename
    )

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/encrypt")
def encrypt_file():
    uploaded = request.files.get("file")

    if not uploaded or not uploaded.filename:
        return result("Please choose a file first."), 400

    filename = uploaded.filename

    if not valid_filename(filename):
        return result("Invalid filename."), 400

    try:
        data = uploaded.read()

        if not data:
            return result("The selected file is empty."), 400

        disk.write_file(filename, data)
        return result(
            f"Encryption successful! {filename} was stored in the virtual disk."
        )
    except Exception:
        app.logger.exception("Encryption failed")
        return result("Encryption failed. Check the VS Code terminal for details."), 500

@app.post("/decrypt")
def decrypt_file():
    filename = request.form.get("filename", "").strip()

    if not valid_filename(filename):
        return result("Please enter a valid original filename."), 400

    try:
        data = disk.read_file(filename)
        output_path = DECRYPTED_DIR / filename
        output_path.write_bytes(data)

        return result(
            f"Decryption successful! The recovered file was saved to decrypted/{filename}."
        )
    except Exception:
        app.logger.exception("Decryption failed")
        return result(
            "Decryption failed. Check the filename, encryption key, and VS Code terminal."
        ), 400

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(error):
    return result("File is too large. The current limit is 16 MB."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

