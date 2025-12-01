import logging
from pathlib import Path
from typing import Optional, Union

from PIL import Image

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
    logo_path: Optional[Union[str, Path]] = None,
    logo_size_percent: int = 20,
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
    logging.debug("Adding data to QR code (%d chars)", len(data))
    qr.add_data(data)
    qr.make(fit=True)
    out_path = Path(output_path)

    # Detect SVG output by file extension and choose appropriate image factory
    if out_path.suffix.lower() == ".svg":
        from qrcode.image.svg import SvgImage

        img = qr.make_image(
            image_factory=SvgImage, fill_color=fill_color, back_color=back_color
        )
        logging.info("Writing QR SVG to %s", out_path)
        img.save(out_path)
        return out_path

    # Raster output (PNG/JPEG...)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    # Optional logo overlay (only for raster formats)
    if logo_path is not None:
        logo_file = Path(logo_path)
        if not logo_file.exists():
            raise FileNotFoundError(f"Logo not found: {logo_file}")
        if not (1 <= logo_size_percent <= 40):
            raise ValueError("logo_size_percent must be between 1 and 40")

        logo = Image.open(logo_file).convert("RGBA")
        qr_w, qr_h = img.size
        max_logo_w = qr_w * logo_size_percent // 100
        max_logo_h = qr_h * logo_size_percent // 100
        logo.thumbnail((max_logo_w, max_logo_h), Image.LANCZOS)

        # Center position
        lx = (qr_w - logo.width) // 2
        ly = (qr_h - logo.height) // 2
        img.alpha_composite(logo, dest=(lx, ly))

    logging.info("Writing QR image to %s", out_path)
    img.save(out_path)
    return out_path


def main() -> None:
    # Default behavior preserved for direct execution
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
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
