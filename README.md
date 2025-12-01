# QR Code Generator

A production-ready Python QR Code Generator with CLI and library interfaces. Generate QR codes from text or URLs, customize colors and sizes, add logo overlays, and export to PNG, JPEG, or SVG formats.

## Features

- **CLI & Library API**: Use as a command-line tool or import as a Python module
- **Multiple Formats**: Output to PNG, JPEG, or SVG (vector)
- **Logo Overlay**: Embed logos in the center of QR codes with automatic scaling
- **Customization**: Control error correction, box size, border, and colors
- **Input Validation**: Graceful error handling with clear user feedback
- **Logging**: Adjustable verbosity with `--verbose` and `--quiet` flags
- **Fully Tested**: Pytest suite with >90% coverage

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Deepak-Kumar-784/QR_Code_Generator.git
cd QR_Code_Generator
```

2. (Optional) Create a virtual environment:

```powershell
# Windows PowerShell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

#### Basic Usage

```powershell
# Generate a simple QR code
python cli.py --data "https://example.com" --out qr.png

# Read data from a file
python cli.py --infile data.txt --out qr.png
```

#### Advanced Options

```powershell
# Custom colors and size
python cli.py --data "Hello World" --out qr.png --fill blue --back yellow --box-size 15 --border 2

# SVG output (vector format)
python cli.py --data "Vector QR" --out qr.svg --ec H

# With logo overlay
python cli.py --data "https://mysite.com" --out branded.png --logo logo.png --logo-size 25 --ec H

# Verbose logging
python cli.py --data "Debug Mode" --out qr.png --verbose
```

#### CLI Options

| Flag          | Description                                     | Default             |
| ------------- | ----------------------------------------------- | ------------------- |
| `--data`      | Data string to encode (use quotes)              | Required\*          |
| `--infile`    | Path to text file with data                     | Required\*          |
| `--out`       | Output image path (extension determines format) | `qr_code_image.png` |
| `--version`   | QR version 1-40 (omit to auto-fit)              | Auto                |
| `--ec`        | Error correction: `L`, `M`, `Q`, `H`            | `H`                 |
| `--box-size`  | Size of each QR box in pixels                   | `10`                |
| `--border`    | Border size (quiet zone)                        | `4`                 |
| `--fill`      | Fill color (name or `#RRGGBB`)                  | `black`             |
| `--back`      | Background color (name or `#RRGGBB`)            | `white`             |
| `--logo`      | Logo image to overlay (PNG recommended)         | None                |
| `--logo-size` | Logo max size as % of QR (1-40)                 | `20`                |
| `--verbose`   | Enable debug logging                            | Off                 |
| `--quiet`     | Suppress info logs                              | Off                 |

\*Either `--data` or `--infile` is required

### Python Library API

```python
from qr_code import generate_qr

# Basic usage
path = generate_qr(
    data="https://example.com",
    output_path="qr.png"
)
print(f"QR code saved to: {path}")

# With customization
path = generate_qr(
    data="Custom QR",
    output_path="custom.png",
    box_size=12,
    border=2,
    fill_color="darkblue",
    back_color="lightgray",
    error_correction="H"
)

# SVG output
path = generate_qr(
    data="Vector QR",
    output_path="vector.svg",
    fill_color="green",
    back_color="white"
)

# With logo overlay
path = generate_qr(
    data="Branded QR",
    output_path="branded.png",
    logo_path="logo.png",
    logo_size_percent=25,
    error_correction="H"
)
```

## Error Correction Levels

| Level | Recovery Capacity | Use Case                 |
| ----- | ----------------- | ------------------------ |
| `L`   | ~7%               | Clean environments       |
| `M`   | ~15%              | General use              |
| `Q`   | ~25%              | Moderate damage expected |
| `H`   | ~30%              | High damage/logo overlay |

**Tip**: Use `H` when adding logo overlays to ensure scannability.

## Examples

### Wi-Fi QR Code

```powershell
python cli.py --data "WIFI:T:WPA;S:MyNetwork;P:MyPassword;;" --out wifi.png --ec H
```

### vCard Contact

```powershell
python cli.py --data "BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD" --out contact.png
```

### Batch Generation (Script Example)

```python
from qr_code import generate_qr

urls = ["https://example.com", "https://example.org", "https://example.net"]
for i, url in enumerate(urls, 1):
    generate_qr(url, f"out/qr_{i}.png")
```

## Development

### Running Tests

```bash
pytest -q              # Quick mode
pytest -v              # Verbose
pytest --cov=qr_code   # With coverage
```

### Project Structure

```
QR_Code_Generator/
├── cli.py              # Command-line interface
├── qr_code.py          # Core QR generation logic
├── requirements.txt    # Dependencies
├── tests/
│   └── test_qr.py     # Test suite
├── LICENSE
└── README.md
```

## Troubleshooting

### PowerShell Special Characters

Wrap URLs/data containing `&`, `?`, or backticks in single quotes:

```powershell
python cli.py --data 'https://example.com?foo=bar&baz=qux' --out qr.png
```

### Logo Not Visible

- Ensure error correction is set to `H` for better recovery
- Use PNG logos with transparency for best results
- Keep `--logo-size` between 15-30% for optimal scannability

### Module Import Errors

If tests fail with `ModuleNotFoundError`, ensure you're in the project root and dependencies are installed:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

Built with:

- [qrcode](https://github.com/lincolnloop/python-qrcode) - QR code generation
- [Pillow](https://python-pillow.org/) - Image processing
