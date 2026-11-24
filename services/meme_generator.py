import io
import os
from PIL import Image, ImageDraw, ImageFont


def _load_font(font_size: int):
    candidate_paths = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except OSError:
                continue
    return ImageFont.load_default()


def _wrap_text(draw, text: str, font, max_width: int):
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = f"{current_line} {word}"
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines


def create_meme_image(photo_bytes: bytes, caption: str, position: str = "bottom") -> bytes:
    """Добавляет подпись в выбранную область фото (top, center, bottom) и возвращает PNG."""
    with Image.open(io.BytesIO(photo_bytes)) as img:
        image = img.convert("RGB")

    width, height = image.size
    draw = ImageDraw.Draw(image)

    font_size = max(24, min(width // 14, 72))
    font = _load_font(font_size)

    horizontal_margin = max(20, int(width * 0.06))
    max_text_width = max(50, width - 2 * horizontal_margin)

    lines = _wrap_text(draw, caption.strip(), font, max_text_width)
    if not lines:
        lines = [caption.strip()]

    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_heights.append(bbox[3] - bbox[1])

    line_spacing = max(6, int(font_size * 0.25))
    total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)
    vertical_margin = max(24, int(height * 0.05))

    if position == "top":
        current_y = vertical_margin
    elif position == "center":
        current_y = max(16, (height - total_text_height) // 2)
    else:
        current_y = max(16, height - total_text_height - vertical_margin)

    stroke_width = max(2, font_size // 14)

    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2

        draw.text(
            (x, current_y),
            line,
            font=font,
            fill="white",
            stroke_width=stroke_width,
            stroke_fill="black",
        )
        current_y += line_heights[idx] + line_spacing

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output.getvalue()