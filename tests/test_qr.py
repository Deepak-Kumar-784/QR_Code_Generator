from pathlib import Path
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qr_code import generate_qr


def test_generate_qr_creates_image(tmp_path: Path) -> None:
    out = tmp_path / "code.png"
    p = generate_qr(
        data="hello world",
        output_path=out,
        box_size=4,
        border=2,
        error_correction="M",
        fill_color="black",
        back_color="white",
    )
    assert p.exists()
    img = Image.open(p)
    try:
        img.verify()
    finally:
        img.close()


def test_generate_qr_svg(tmp_path: Path) -> None:
    out = tmp_path / "vector.svg"
    p = generate_qr(
        data="vector test",
        output_path=out,
        box_size=4,
        border=2,
        error_correction="M",
        fill_color="black",
        back_color="white",
    )
    assert p.exists()
    text = out.read_text(encoding="utf-8")
    assert "<svg" in text.lower()


def test_generate_qr_with_logo(tmp_path: Path) -> None:
    # Create a simple logo image
    logo_path = tmp_path / "logo.png"
    logo_img = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    logo_img.save(logo_path)

    out = tmp_path / "with_logo.png"
    p = generate_qr(
        data="logo test",
        output_path=out,
        box_size=8,
        border=4,
        error_correction="H",
        fill_color="black",
        back_color="white",
        logo_path=logo_path,
        logo_size_percent=25,
    )
    assert p.exists()
    img = Image.open(p)
    try:
        # Basic assertion that center pixel differs from plain fill color (overlay present)
        w, h = img.size
        center_pixel = img.convert("RGBA").getpixel((w // 2, h // 2))
        assert center_pixel[0] == 255  # red logo component
    finally:
        img.close()
