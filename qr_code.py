# import qrcode as qr
# img = qr.make(
#     "https://www.youtube.com/watch?v=p5W90_d1sDw&list=RDp5W90_d1sDw&start_radio=1"
# )
# img.save("wscube_youtube.jpeg")

import qrcode
from PIL import Image

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data("YOUR_URL_HERE")
qr.make(fit=True)
img = qr.make(fill_color="red", back_color="black")
img.save("qr_code_image.jpeg")
