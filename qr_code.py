# import qrcode as qr
# img = qr.make(
#     "https://www.youtube.com/watch?v=p5W90_d1sDw&list=RDp5W90_d1sDw&start_radio=1"
# )
# img.save("wscube_youtube.jpeg")

# Import the required libraries
import qrcode  # Library to generate QR codes
from PIL import Image  # Library to handle images (used by qrcode)

# Create a QRCode object with customization options
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR code (1 = smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction (can recover from ~30% damage)
    box_size=10,  # Size of each "box" in the QR code
    border=4,  # Thickness of the border (default is 4)
)

# Add the URL or data you want to encode into the QR code
qr.add_data("YOUR_URL_HERE")

# Generate the QR code with the data added
qr.make(fit=True)  # Adjust the QR code size automatically to fit the data

# Create an image of the QR code with custom colors
img = qr.make(
    fill_color="red", back_color="black"
)  # QR boxes in red, background in black

# Save the QR code image as a file
img.save("qr_code_image.jpeg")
