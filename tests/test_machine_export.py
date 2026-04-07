from io import BytesIO

from PIL import Image

from backend.machine_export import prepare_for_machine


def sample_image() -> Image.Image:
    img = Image.new("RGB", (800, 1200), color=(180, 160, 140))
    return img


def test_sauno_returns_grayscale_bmp():
    data, ext, mime = prepare_for_machine(sample_image(), "Sauno", dpi=90)
    assert ext == "bmp"
    assert mime == "image/bmp"

    out = Image.open(BytesIO(data))
    assert out.mode == "L"


def test_almaz_returns_1bit_bmp():
    data, ext, _ = prepare_for_machine(sample_image(), "Almaz", dpi=90)
    assert ext == "bmp"

    out = Image.open(BytesIO(data))
    assert out.mode == "1"


def test_laser_m_inverts_image():
    dark = Image.new("RGB", (100, 100), color=(0, 0, 0))
    data, _, _ = prepare_for_machine(dark, "Laser-M", dpi=90, target_mm=(50, 50))
    out = Image.open(BytesIO(data)).convert("L")
    assert out.getextrema()[1] >= 245
