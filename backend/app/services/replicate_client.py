from __future__ import annotations

from io import BytesIO
from typing import Any

from PIL import Image

from app.config import get_settings

try:
    import replicate
except Exception:  # pragma: no cover
    replicate = None


def run_replicate_image(model: str, input_payload: dict[str, Any]) -> Image.Image | None:
    settings = get_settings()
    if not settings.replicate_api_token or replicate is None:
        return None

    client = replicate.Client(api_token=settings.replicate_api_token)
    output = client.run(model, input=input_payload)

    if isinstance(output, list):
        output = output[0]
    if hasattr(output, "read"):
        data = output.read()
    elif isinstance(output, bytes):
        data = output
    else:
        return None

    return Image.open(BytesIO(data)).convert("RGB")
