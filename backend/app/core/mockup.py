from __future__ import annotations

from PIL import Image, ImageOps


STONE_COLORS = {
    "gabbro": (30, 30, 35),
    "marble": (210, 210, 205),
}


def apply_stone_mockup(portrait: Image.Image, stone: str = "gabbro") -> Image.Image:
    base_color = STONE_COLORS.get(stone, STONE_COLORS["gabbro"])
    canvas = Image.new("RGB", portrait.size, color=base_color)
    engraving = ImageOps.grayscale(portrait).convert("RGB")
    return Image.blend(canvas, engraving, alpha=0.35)
