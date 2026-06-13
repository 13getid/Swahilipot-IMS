import io
import base64
import qrcode

def make_qr_data_uri(url):
    image = qrcode.make(url)
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    png_bytes = buffer.getvalue()

    b64 = base64.b64decode(png_bytes).decode('ascii')
    return f'data:image/png;base64,{b64}'