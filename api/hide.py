import os
from sanic import Sanic, response

app = Sanic()


@app.route("/<path:path>", methods=["POST"])
async def index(request, path):
    if "files" not in request.files:
        return response.json({}, status=400)

    files = request.files["files"]
    if len(files) < 2:
        return response.json({}, status=400)

    cover_img, payload_file = files[:2]
    cover_name, cover_ext = os.path.splitext(cover_img.name)
    cover_buffer = cover_img.body
    payload_buffer = payload_file.body

    #
    # process
    #

    return response.json({})
