from datetime import datetime as dt
import os

import firebase_admin
from firebase_admin import credentials, storage


cred = credentials.Certificate(
    os.path.join(os.path.dirname(__file__), "../service-account-key.json")
)
firebase_admin.initialize_app(cred, {"storageBucket": "steganopy.appspot.com"})
bucket = storage.bucket()


def save_to_storage(filename: str, data: bytes, mime: str) -> str:
    name, ext = os.path.splitext(filename)

    blob = bucket.blob(f"{name}-{round(dt.utcnow().timestamp())}{ext}")
    blob.upload_from_string(data, content_type=mime)
    blob.make_public()

    return blob.public_url
