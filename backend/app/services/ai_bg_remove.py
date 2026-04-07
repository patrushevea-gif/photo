from __future__ import annotations

from PIL import Image


def remove_background(image: Image.Image) -> Image.Image:
    # Placeholder for rembg/segment-anything API; keeps transparent pipeline ready.
    return image.convert("RGBA")
