from __future__ import annotations

from PIL import Image, ImageEnhance, ImageOps


DEFAULT_DPI = 90


def export_sauno(image: Image.Image, dpi: int = DEFAULT_DPI) -> Image.Image:
    gray = ImageOps.grayscale(image)
    boosted = ImageEnhance.Contrast(gray).enhance(1.5)
    return boosted.convert("L")
