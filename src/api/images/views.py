import os
from os.path import exists

from flask import Blueprint, request, send_file

from badger.badger import get_image, generate_badge

api = Blueprint("images", __name__)


@api.route("/api/images/badge", methods=["POST"])
def create_badge():
    params = request.get_json()
    selfie_url = params.get("selfie_url")
    if selfie_url is None:
        return "bad request: selfie_url required", 400

    selfie = get_image(selfie_url)
    if selfie is None:
        return "can't get selfie", 500

    name_1 = params.get("name_1", "")
    name_2 = params.get("name_2", "")
    name_3 = params.get("name_3", "")

    filename = generate_badge(selfie, name_1, name_2, name_3)

    return {"badge_url": f"https://images.easytap.io/media/{filename}"}


@api.route("/media/<filename>", methods=["GET"])
def get_badge(filename):
    fpath = f"{os.environ.get('MEDIA_PATH')}/{filename}"
    if not exists(fpath):
        return "image not found", 404

    return send_file(fpath, mimetype='image/gif')
