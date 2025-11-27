import qrcode as qr

img = qr.make(
    "https://www.youtube.com/watch?v=p5W90_d1sDw&list=RDp5W90_d1sDw&start_radio=1"
)
img.save("wscube_youtube.jpeg")
