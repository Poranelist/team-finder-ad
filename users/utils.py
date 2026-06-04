import hashlib
import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from core.constants import (AVATAR_COLOR_PALETTE, AVATAR_FONT_SIZE,
                            AVATAR_SIZE, AVATAR_TEXT_COLOR, FONT_PATHS)


def create_avatar(name, surname, email):

    initials = (name[:1] + surname[:1] or "U").upper()
    if not initials:
        initials = "U"

    bg_color = random.choice(AVATAR_COLOR_PALETTE)

    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color=bg_color)

    drawer = ImageDraw.Draw(image)

    font = None
    for font_path in FONT_PATHS:
        try:
            font = ImageFont.truetype(font_path, AVATAR_FONT_SIZE)
            break
        except OSError:
            continue

    if font is None:
        font = ImageFont.load_default()

    bbox = drawer.textbbox((0, 0), initials, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position_x = (AVATAR_SIZE - text_width) / 2 - bbox[0]
    position_y = (AVATAR_SIZE - text_height) / 2 - bbox[1]

    drawer.text((position_x, position_y), initials,
                fill=AVATAR_TEXT_COLOR, font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    filename_hash = hashlib.md5(email.encode()).hexdigest()[:10]

    return ContentFile(buffer.read(), name=f"avatar_{filename_hash}.png")
