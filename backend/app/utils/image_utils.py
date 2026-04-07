from __future__ import annotations

import base64
from io import BytesIO
from PIL import Image, ImageOps


def read_image(data: bytes) -> Image.Image:
    return Image.open(BytesIO(data)).convert("RGB")


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    buf = BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def image_to_base64(image: Image.Image, fmt: str = "PNG") -> str:
    encoded = base64.b64encode(image_to_bytes(image, fmt=fmt)).decode("utf-8")
    return f"data:image/{fmt.lower()};base64,{encoded}"


def fit_to_size(image: Image.Image, width: int, height: int) -> Image.Image:
    return ImageOps.fit(image, (width, height), method=Image.Resampling.LANCZOS)
