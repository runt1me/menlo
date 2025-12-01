import os
import time
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.environ.get("FLASK_API_KEY")
TOOLS_DIR = "/root/tools"

app = Flask(__name__)

def require_api_key():
    """Simple API key check using X-API-Key header."""
    if not API_KEY:
        abort(500, description="Server API key not configured")

    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        abort(401, description="Invalid or missing API key")

@app.route("/push", methods=["POST"])
def push():
    """
    Receive a file and save it to /root/tools with a timestamp suffix.

    Example:
        test.txt -> /root/tools/test.txt.1701461234
    """
    require_api_key()

    if "file" not in request.files:
        abort(400, description="No file part in the request")

    uploaded = request.files["file"]
    if uploaded.filename == "":
        abort(400, description="No selected file")

    # Sanitize filename
    original_name = secure_filename(uploaded.filename)
    if not original_name:
        abort(400, description="Invalid filename")

    epoch = int(time.time())
    dest_name = f"{original_name}.{epoch}"
    dest_path = os.path.join(TOOLS_DIR, dest_name)

    # Save the file
    uploaded.save(dest_path)

    return jsonify(
        {
            "status": "ok",
            "saved_as": dest_name,
            "full_path": dest_path,
            "epoch": epoch,
        }
    ), 201

@app.route("/")
def hello():
    return "Menlo is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

