from pathlib import Path
from typing import Optional, Union

import qrcode


def _map_error_correction(level: str) -> int:
    mapping = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    return mapping.get(level.upper(), qrcode.constants.ERROR_CORRECT_H)


def generate_qr(
    data: str,
    output_path: Union[str, Path],
    *,
    version: Optional[int] = None,
    error_correction: str = "H",
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
) -> Path:
    """Generate a QR code image and save it to output_path.

    Returns the path to the written image file.
    """
    ec = _map_error_correction(error_correction)
    qr = qrcode.QRCode(
        version=version or 1,
        error_correction=ec,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    out_path = Path(output_path)
    img.save(out_path)
    return out_path


def main() -> None:
    # Default behavior preserved for direct execution
    generate_qr(
        data="YOUR_URL_HERE",
        output_path="qr_code_image.jpeg",
        error_correction="H",
        box_size=10,
        border=4,
        fill_color="red",
        back_color="black",
    )


if __name__ == "__main__":
    main()
