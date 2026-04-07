from __future__ import annotations

from PIL import Image, ImageOps


DEFAULT_DPI = 90


def export_mirtels(image: Image.Image, dpi: int = DEFAULT_DPI) -> Image.Image:
    gray = ImageOps.grayscale(image)
    return gray.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
