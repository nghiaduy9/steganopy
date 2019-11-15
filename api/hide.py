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

    secret_file, cover_img = files[:2]
    secret_body = secret_file.body
    cover_name, cover_ext = os.path.splitext(cover_img.name)
    cover_body = cover_img.body

    #
    # process
    #

    return response.json({})
