from pathlib import Path
import sys
from pathlib import Path

from PIL import Image

# Ensure project root is on sys.path for importing qr_code module
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
