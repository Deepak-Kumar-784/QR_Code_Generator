from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from PIL import ImageColor

from qr_code import generate_qr


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate QR codes from data or files.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--data", type=str, help="Data string to encode (use quotes)")
    src.add_argument("--infile", type=Path, help="Path to a text file with data")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("qr_code_image.png"),
        help="Output image path (extension determines format; use .svg for vector)",
    )
    p.add_argument(
        "--version", type=int, default=None, help="QR version 1-40 (omit to auto-fit)"
    )
    p.add_argument(
        "--ec", choices=["L", "M", "Q", "H"], default="H", help="Error correction level"
    )
    p.add_argument("--box-size", type=int, default=10, help="Size of each QR box")
    p.add_argument("--border", type=int, default=4, help="Border size (quiet zone)")
    p.add_argument(
        "--fill", type=str, default="black", help="Fill color (name or #RRGGBB)"
    )
    p.add_argument(
        "--back", type=str, default="white", help="Background color (name or #RRGGBB)"
    )
    v = p.add_mutually_exclusive_group()
    v.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    v.add_argument("--quiet", action="store_true", help="Suppress informational logs")
    return p.parse_args(argv)


def _validate_colors(fill: str, back: str) -> None:
    # Will raise ValueError if invalid
    ImageColor.getrgb(fill)
    ImageColor.getrgb(back)


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    if args.quiet:
        level = logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    data: str
    if args.data is not None:
        data = args.data
    else:
        if not args.infile.exists():
            print(f"error: infile not found: {args.infile}", file=sys.stderr)
            return 2
        data = args.infile.read_text(encoding="utf-8").strip()

    if not data:
        print("error: data is empty", file=sys.stderr)
        return 2

    if args.box_size < 1 or args.border < 0:
        print("error: --box-size must be >=1 and --border >=0", file=sys.stderr)
        return 2

    try:
        _validate_colors(args.fill, args.back)
    except Exception as e:
        print(f"error: invalid color(s): {e}", file=sys.stderr)
        return 2

    out: Path = args.out
    parent = out.parent
    if parent and not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"error: cannot create directory {parent}: {e}", file=sys.stderr)
            return 2

        try:
            generate_qr(
                data=data,
                output_path=args.out,
                version=args.version,
                error_correction=args.ec,
                box_size=args.box_size,
                border=args.border,
                fill_color=args.fill,
                back_color=args.back,
                logo_path=args.logo,
                logo_size_percent=args.logo_size,
            )
        except Exception as e:
            logging.error("Failed to generate QR code: %s", e)
            return 2
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
