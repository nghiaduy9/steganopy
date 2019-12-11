from io import BytesIO
from PIL import Image

from sanic import Sanic, response

from api._stegano import detect


app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    if "files" not in request.files:
        return response.json({"error": "BAD_INPUT"})
    files = request.files["files"]
    if len(files) < 1:
        return response.json({"error": "BAD_INPUT"})

    img_file = files[0]
    img_buffer = img_file.body

    img = Image.open(BytesIO(img_buffer))

    return response.json({"result": detect(img)})
