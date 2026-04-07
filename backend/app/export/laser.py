from __future__ import annotations

from PIL import Image, ImageOps


DEFAULT_DPI = 90


def export_laser(image: Image.Image, dpi: int = DEFAULT_DPI) -> Image.Image:
    gray = ImageOps.grayscale(image)
    inverted = ImageOps.invert(gray)
    return inverted.convert("L")
