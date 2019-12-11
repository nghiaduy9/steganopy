from io import BytesIO
from PIL import Image

from sanic import Sanic, response

from api._stegano import conceal, validate_payload_size
from api._utils import save_to_storage


app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    if "files" not in request.files:
        return response.json({"error": "BAD_INPUT"})
    files = request.files["files"]
    if len(files) < 2:
        return response.json({"error": "BAD_INPUT"})

    cover_img, payload_file = files[:2]
    cover_name = cover_img.name
    cover_buffer = cover_img.body
    payload_buffer = payload_file.body

    img = Image.open(BytesIO(cover_buffer))

    if not validate_payload_size(img, payload_buffer):
        return response.json({"error": "PAYLOAD_TOO_LARGE"})

    try:
        output_buffer = conceal(img, payload_buffer)
        url = save_to_storage(cover_name, output_buffer, "image/png")
        return response.json({"url": url})
    except Exception as e:
        print(e)
        return response.json({}, status=500)
