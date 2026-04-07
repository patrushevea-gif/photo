from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Literal

import numpy as np
from PIL import Image, ImageOps


MachineType = Literal["Sauno", "Mirtels", "Graphica", "Almaz", "Zubr", "Laser-M", "Bryullov"]


@dataclass(frozen=True)
class MachineSpec:
    output_format: Literal["BMP", "JPEG", "PNG"]
    grayscale_mode: Literal["L", "1"]
    invert: bool = False
    dithering: Literal["none", "floyd", "stucki"] = "none"


MACHINE_SPECS: dict[str, MachineSpec] = {
    "Sauno": MachineSpec(output_format="BMP", grayscale_mode="L"),
    "Mirtels": MachineSpec(output_format="BMP", grayscale_mode="L", dithering="floyd"),
    "Graphica": MachineSpec(output_format="BMP", grayscale_mode="L"),
    "Almaz": MachineSpec(output_format="BMP", grayscale_mode="1", dithering="stucki"),
    "Zubr": MachineSpec(output_format="BMP", grayscale_mode="L"),
    "Laser-M": MachineSpec(output_format="BMP", grayscale_mode="L", invert=True),
    "Bryullov": MachineSpec(output_format="PNG", grayscale_mode="L", invert=True),
}


def _auto_levels(gray: Image.Image) -> Image.Image:
    arr = np.asarray(gray, dtype=np.uint8)
    lo = int(np.percentile(arr, 1))
    hi = int(np.percentile(arr, 99))
    if hi <= lo:
        return gray
    stretched = np.clip((arr - lo) * 255.0 / (hi - lo), 0, 255).astype(np.uint8)
    return Image.fromarray(stretched, mode="L")


def _resize_mm(image: Image.Image, width_mm: int = 300, height_mm: int = 400, dpi: int = 90) -> Image.Image:
    width_px = int(round(width_mm / 25.4 * dpi))
    height_px = int(round(height_mm / 25.4 * dpi))
    return ImageOps.fit(image, (width_px, height_px), method=Image.Resampling.LANCZOS)


def _stucki_dither(gray: Image.Image) -> Image.Image:
    arr = np.asarray(gray, dtype=np.float32)
    h, w = arr.shape
    out = np.zeros_like(arr, dtype=np.uint8)

    # Stucki matrix weights / 42
    diffusion = [
        (1, 0, 8),
        (2, 0, 4),
        (-2, 1, 2),
        (-1, 1, 4),
        (0, 1, 8),
        (1, 1, 4),
        (2, 1, 2),
        (-2, 2, 1),
        (-1, 2, 2),
        (0, 2, 4),
        (1, 2, 2),
        (2, 2, 1),
    ]

    for y in range(h):
        for x in range(w):
            old = arr[y, x]
            new = 255.0 if old >= 128 else 0.0
            out[y, x] = 255 if new == 255 else 0
            err = old - new
            for dx, dy, weight in diffusion:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    arr[ny, nx] += err * (weight / 42.0)

    return Image.fromarray(out, mode="L").convert("1")


def prepare_for_machine(
    image: Image.Image,
    machine_type: MachineType,
    dpi: int = 90,
    target_mm: tuple[int, int] = (300, 400),
) -> tuple[bytes, str, str]:
    """Prepare a portrait for stone engraving machines.

    Returns tuple: (file_bytes, extension, mime_type).
    """
    if machine_type not in MACHINE_SPECS:
        supported = ", ".join(sorted(MACHINE_SPECS.keys()))
        raise ValueError(f"Unsupported machine_type '{machine_type}'. Supported: {supported}")

    spec = MACHINE_SPECS[machine_type]
    prepared = _resize_mm(image.convert("RGB"), target_mm[0], target_mm[1], dpi=dpi)
    prepared = ImageOps.grayscale(prepared)
    prepared = _auto_levels(prepared)

    if spec.invert:
        prepared = ImageOps.invert(prepared)

    if spec.dithering == "floyd":
        prepared = prepared.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
    elif spec.dithering == "stucki":
        prepared = _stucki_dither(prepared)
    elif spec.grayscale_mode == "L":
        prepared = prepared.convert("L")

    extension = "bmp" if spec.output_format == "BMP" else ("jpg" if spec.output_format == "JPEG" else "png")
    mime_type = f"image/{'jpeg' if extension == 'jpg' else extension}"

    output = BytesIO()
    prepared.save(output, format=spec.output_format, dpi=(dpi, dpi))
    return output.getvalue(), extension, mime_type
