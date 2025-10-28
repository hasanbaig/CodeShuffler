import random

from PIL import Image, ImageDraw, ImageFont


def shuffle_sol(correct_sol):
    random_code = random.sample(correct_sol, k=len(correct_sol))
    # removing the indents for programming blocks
    for el in range(len(random_code)):
        random_code[el] = (
            f"({el+1}) " + random_code[el]
        )  # .strip()        #Remove strip() function to include tabs
    return random_code


def sequence_similarity(seq1, seq2):
    set1 = set(seq1)
    set2 = set(seq2)
    return len(set1.intersection(set2))


def print_code(in_code, message="##### Code #####"):
    print()
    print(message)
    for line in in_code:
        print(line)


def convert_to_image(shuffled_sol, file_name):
    code_text = "\n".join(line.rstrip() for line in shuffled_sol)
    fnt = ImageFont.truetype("lib/fonts/static/SourceCodePro-Medium.ttf", 15)
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
    file_path = f"images/{file_name}.png"
    img.save(file_path)
