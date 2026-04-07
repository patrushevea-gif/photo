from io import BytesIO

from PIL import Image

from backend.app.export import export_for_machine


def sample_image() -> Image.Image:
    return Image.new("RGB", (800, 1200), color=(100, 120, 140))


def test_sauno_is_grayscale_bmp():
    data, ext, mime = export_for_machine(sample_image(), machine="sauno")
    assert ext == "bmp"
    assert mime == "image/bmp"
    out = Image.open(BytesIO(data))
    assert out.mode == "L"


def test_mirtels_is_binary_bmp():
    data, ext, _ = export_for_machine(sample_image(), machine="mirtels")
    assert ext == "bmp"
    out = Image.open(BytesIO(data))
    assert out.mode == "1"


def test_laser_inverts_black_to_white():
    dark = Image.new("RGB", (200, 200), color=(0, 0, 0))
    data, _, _ = export_for_machine(dark, machine="laser")
    out = Image.open(BytesIO(data)).convert("L")
    assert out.getextrema()[1] > 245


def test_diamond_binary_mode():
    data, ext, _ = export_for_machine(sample_image(), machine="diamond")
    assert ext == "bmp"
    out = Image.open(BytesIO(data))
    assert out.mode == "1"
