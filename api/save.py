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
    if "files" not in request.files:
        return response.json({}, status=400)

    files = request.files["files"]
    if not len(files):
        return response.json({}, status=400)

    img = files[0]
    img_name, img_ext = os.path.splitext(img.name)
    img_body = img.body
    img_mime = img.type

    blob = bucket.blob(f"{img_name}-{round(dt.utcnow().timestamp())}{img_ext}")
    blob.upload_from_string(img_body, content_type=img_mime)
    blob.make_public()

    return response.json({"url": blob.public_url})
