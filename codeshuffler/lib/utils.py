import os
import sys

from PIL import Image, ImageDraw, ImageFont


def print_code(in_code, message="##### Code #####"):
    print()
    print(message)
    for line in in_code:
        print(line)


def convert_to_image(shuffled_sol, file_name):
    code_text = "\n".join(line.rstrip() for line in shuffled_sol)
    fnt = ImageFont.truetype("codeshuffler/lib/fonts/static/SourceCodePro-Medium.ttf", 15)
    # temporary surface to measure bounding box
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.multiline_textbbox((0, 0), code_text, font=fnt, spacing=4)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    # padding
    pad_x, pad_y = 20, 20
    img = Image.new("RGB", (width + 2 * pad_x, height + 2 * pad_y), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.multiline_text((pad_x, pad_y), code_text, font=fnt, fill=(0, 0, 0), spacing=4)
    file_path = f"codeshuffler/gui/outputs/{file_name}.png"
    img.save(file_path)


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def download_image(shuffled_sol, file_path):
    code_text = "\n".join(line.rstrip() for line in shuffled_sol)
    fnt = ImageFont.truetype("codeshuffler/lib/fonts/static/SourceCodePro-Medium.ttf", 15)
    # temporary surface to measure bounding box
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.multiline_textbbox((0, 0), code_text, font=fnt, spacing=4)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    # padding
    pad_x, pad_y = 20, 20
    img = Image.new("RGB", (width + 2 * pad_x, height + 2 * pad_y), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.multiline_text((pad_x, pad_y), code_text, font=fnt, fill=(0, 0, 0), spacing=4)
    img.save(file_path)
