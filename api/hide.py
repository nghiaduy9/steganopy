import os
from sanic import Sanic, response

from api._stegano import hide
from api._utils import save_to_storage


app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    if "files" not in request.files:
        return response.json({}, status=400)

    files = request.files["files"]
    if len(files) < 2:
        return response.json({}, status=400)

    cover_img, payload_file = files[:2]
    cover_buffer = cover_img.body
    payload_buffer = payload_file.body

    try:
        output_buffer = hide(cover_buffer, payload_buffer)
        url = save_to_storage(cover_img.name, output_buffer, "image/png")
        return response.json({"url": url})
    except Exception as e:
        print(e)
        return response.json({}, status=500)
