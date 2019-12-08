from datetime import datetime as dt
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from sanic import Sanic, response

cred = credentials.Certificate(
    os.path.join(os.path.dirname(__file__), "../service-account-key.json")
)
firebase_admin.initialize_app(cred, {"storageBucket": "steganopy.appspot.com"})
bucket = storage.bucket()
app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    """Save a static file to Firebase Storage and return the URL."""

    if "files" not in request.files:
        return response.json({}, status=400)

    files = request.files["files"]
    if not len(files):
        return response.json({}, status=400)

    file = files[0]
    file_name, file_ext = os.path.splitext(file.name)
    file_buffer = file.body
    file_mime = file.type

    blob = bucket.blob(f"{file_name}-{round(dt.utcnow().timestamp())}{file_ext}")
    blob.upload_from_string(file_buffer, content_type=file_mime)
    blob.make_public()

    return response.json({"url": blob.public_url})
