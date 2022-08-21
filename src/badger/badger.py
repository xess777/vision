import os
from hashlib import sha256

import cv2
import numpy as np
import requests


def get_image(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return None

    image_as_np = np.frombuffer(resp.content, dtype=np.uint8)
    image = cv2.imdecode(image_as_np, flags=1)

    return image


def generate_badge(image_selfie, name_1, name_2, name_3) -> str:
    badger_template_path = os.environ.get("BADGER_TEMPLATE")
    image_back = cv2.imread(badger_template_path)

    fix_width_selfie = 440
    fix_height_selfie = 280

    fix_width_back = 800
    fix_height_back = 480

    image_selfie_resized = cv2.resize(
        image_selfie, (fix_height_selfie, fix_width_selfie)
    )
    image_back_resized = cv2.resize(image_back, (fix_height_back, fix_width_back))

    image_back_resized[180:620, 100:380, :] = image_selfie_resized
    image_back_resized[620:, :, :] = (255, 255, 255)

    txt_merged_up = f"{name_2} {name_1}"
    txt_merged_down = name_3

    x_coord_up = 120
    y_coord_up = 670
    coordinates_txt_up = (x_coord_up, y_coord_up)

    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 1.5

    txt_color = (250, 0, 90)

    txt_thickness = 2

    image_back_resized = cv2.putText(
        image_back_resized,
        txt_merged_up,
        coordinates_txt_up,
        font,
        font_scale,
        txt_color,
        txt_thickness,
    )

    x_coord_down = 120
    y_coord_down = 720
    coordinates_txt_down = (x_coord_down, y_coord_down)

    image_back_resized = cv2.putText(
        image_back_resized,
        txt_merged_down,
        coordinates_txt_down,
        font,
        font_scale,
        txt_color,
        txt_thickness,
    )

    is_success, im_buf_arr = cv2.imencode(".png", image_back_resized)
    byte_im = im_buf_arr.tobytes()

    h1 = sha256()
    h1.update(byte_im)
    image_hash = h1.hexdigest()
    filename = f"{image_hash}.png"
    abs_path = f"{os.environ.get('MEDIA_PATH')}/{image_hash}.png"

    cv2.imwrite(abs_path, image_back_resized)

    return filename

