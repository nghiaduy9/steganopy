import os
from sanic import Sanic, response

from api._stegano import reveal


app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    if "files" not in request.files:
        return response.json({}, status=400)
    files = request.files["files"]
    if len(files) < 1:
        return response.json({}, status=400)

    img_file = files[0]
    img_buffer = img_file.body

    try:
        payload_buffer = reveal(img_buffer)
        return response.raw(payload_buffer)
    except Exception as e:
        print(e)
        return response.json({}, status=500)
