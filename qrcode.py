import qrcode
import qrcode.image.svg


img = qrcode.make('https://yingx110-tesdemo-home-interface-rwnje1.streamlit.app/', image_factory=qrcode.image.svg.SvgImage)
with open('qr.svg', 'wb') as qr:
    img.save(qr)