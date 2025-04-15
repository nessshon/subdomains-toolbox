from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR / "data" / "fonts" / "JetBrainsMono-ExtraBold.ttf"

TEXT_COLOR = (0, 0, 0)
FRAME_FILL = (255, 255, 255)


def measure_text(
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont
) -> Tuple[int, int]:
    l, t, r, b = draw.textbbox((0, 0), text, font=font, anchor="lt")
    return r - l, b - t


def ellipsize(text: str, max_length: int = 28) -> str:
    if len(text) <= max_length:
        return text
    return f"{text[:13]}...{text[-12:]}"


def get_dynamic_font_size(
        draw: ImageDraw.ImageDraw,
        text: str,
        font_path: str,
        max_size: int,
        min_size: int,
        max_width: int,
        padding: int,
) -> int:
    for size in range(max_size, min_size - 1, -1):
        font = ImageFont.truetype(font_path, size)
        text_width, _ = measure_text(draw, text, font)
        if text_width + 2 * padding <= max_width:
            return size
    return min_size


def draw_centered_text(
        draw: ImageDraw.ImageDraw,
        image: Image.Image,
        text: str,
        font_path: str,
        style: dict
) -> None:
    font_size = get_dynamic_font_size(
        draw, text, font_path,
        style["max_font_size"],
        style["min_font_size"],
        image.width - 2 * style["min_side_margin"],
        style["side_padding"]
    )

    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = measure_text(draw, text, font)

    frame_top = style["margin"]
    frame_bottom = image.height - style["margin"]
    frame_height = frame_bottom - frame_top

    ideal_left = (image.width - text_width) / 2 - style["side_padding"]
    ideal_right = (image.width + text_width) / 2 + style["side_padding"]
    frame_left = max(ideal_left, style["min_side_margin"])
    frame_right = min(ideal_right, image.width - style["min_side_margin"])

    draw.rounded_rectangle(
        (frame_left, frame_top, frame_right, frame_bottom),
        radius=style["frame_radius"],
        fill=style["frame_fill"]
    )

    text_x = frame_left + (frame_right - frame_left - text_width) / 2
    text_y = frame_top + (frame_height - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill=style["text_color"], anchor="lt")


def draw_bottom_text(
        draw: ImageDraw.ImageDraw,
        image: Image.Image,
        text: str,
        font_path: str,
        style: dict
) -> None:
    max_width = image.width - 2 * (style["min_side_margin"] + style["side_padding"])

    font_size = get_dynamic_font_size(
        draw, text, font_path,
        style["max_font_size"],
        style["min_font_size"],
        max_width,
        0
    )

    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = measure_text(draw, text, font)

    text_x = (image.width - text_width) / 2
    text_y = image.height - text_height - style["margin"]
    draw.text((text_x, text_y), text, font=font, fill=style["text_color"], anchor="lt")


def generate_image(
        domain: str,
        subdomain: Optional[str] = None,
        tld: Optional[str] = "ton",
        *,
        max_font_size: int = 100,
        min_font_size: int = 10,
        margin: int = 380,
        side_padding: int = 67,
        min_side_margin: int = 100,
        frame_radius: int = 77,
        bottom_text_margin: int = 100,
        bottom_max_font_size: int = 40,
        bottom_min_font_size: int = 20,
        bottom_side_padding: int = 20,
) -> bytes:
    length = min(len(subdomain or domain), 11)
    header_text = ellipsize(f"{subdomain or domain}.{tld}")
    bottom_text = ellipsize(f"{subdomain}.{domain}.{tld}") if subdomain else None

    image = Image.open(BASE_DIR / "data" / "backgrounds" / tld / f"{length}.png")
    draw = ImageDraw.Draw(image)

    header_style = {
        "max_font_size": max_font_size,
        "min_font_size": min_font_size,
        "margin": margin,
        "side_padding": side_padding,
        "min_side_margin": min_side_margin,
        "frame_radius": frame_radius,
        "frame_fill": FRAME_FILL,
        "text_color": TEXT_COLOR,
    }

    bottom_style = {
        "max_font_size": bottom_max_font_size,
        "min_font_size": bottom_min_font_size,
        "margin": bottom_text_margin,
        "side_padding": bottom_side_padding,
        "min_side_margin": min_side_margin,
        "text_color": TEXT_COLOR,
    }

    draw_centered_text(draw, image, header_text, str(FONT_PATH), header_style)

    if bottom_text:
        draw_bottom_text(draw, image, bottom_text, str(FONT_PATH), bottom_style)

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()
