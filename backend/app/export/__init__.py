from __future__ import annotations

from io import BytesIO
from typing import Literal
from PIL import Image, ImageOps

from .diamond import export_diamond
from .laser import export_laser
from .mirtels import export_mirtels
from .sauno import export_sauno

MachineType = Literal["sauno", "mirtels", "laser", "diamond"]


def _resize_for_stone(image: Image.Image, width_cm: int = 20, height_cm: int = 30, dpi: int = 90) -> Image.Image:
    width_px = int(round(width_cm / 2.54 * dpi))
    height_px = int(round(height_cm / 2.54 * dpi))
    return ImageOps.fit(image.convert("RGB"), (width_px, height_px), method=Image.Resampling.LANCZOS)


def export_for_machine(image: Image.Image, machine: MachineType, dpi: int = 90) -> tuple[bytes, str, str]:
    base = _resize_for_stone(image, dpi=dpi)

    if machine == "sauno":
        prepared, ext = export_sauno(base, dpi=dpi), "bmp"
    elif machine == "mirtels":
        prepared, ext = export_mirtels(base, dpi=dpi), "bmp"
    elif machine == "laser":
        prepared, ext = export_laser(base, dpi=dpi), "bmp"
    elif machine == "diamond":
        prepared, ext = export_diamond(base), "bmp"
    else:
        raise ValueError(f"Unsupported machine: {machine}")

    out = BytesIO()
    prepared.save(out, format="BMP", dpi=(dpi, dpi))
    return out.getvalue(), ext, f"image/{ext}"
