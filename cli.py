from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from qr_code import generate_qr


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate QR codes from data or files.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--data", type=str, help="Data string to encode (use quotes)")
    src.add_argument("--infile", type=Path, help="Path to a text file with data")
    p.add_argument("--out", type=Path, default=Path("qr_code_image.png"), help="Output image path (extension determines format)")
    p.add_argument("--version", type=int, default=None, help="QR version 1-40 (omit to auto-fit)")
    p.add_argument("--ec", choices=["L", "M", "Q", "H"], default="H", help="Error correction level")
    p.add_argument("--box-size", type=int, default=10, help="Size of each QR box")
    p.add_argument("--border", type=int, default=4, help="Border size (quiet zone)")
    p.add_argument("--fill", type=str, default="black", help="Fill color (name or #RRGGBB)")
    p.add_argument("--back", type=str, default="white", help="Background color (name or #RRGGBB)")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    data: str
    if args.data is not None:
        data = args.data
    else:
        data = args.infile.read_text(encoding="utf-8")

    generate_qr(
        data=data,
        output_path=args.out,
        version=args.version,
        error_correction=args.ec,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill,
        back_color=args.back,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
