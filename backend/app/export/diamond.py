from __future__ import annotations

from PIL import Image, ImageOps


def export_diamond(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    return gray.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
