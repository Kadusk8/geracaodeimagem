from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/gerar-imagem', methods=['GET'])
def gerar_imagem():
    img_url = request.args.get('img_url')
    titulo = request.args.get('titulo')

    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(img)
    width, height = img.size

    font_size = int(height * 0.06)
    font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), titulo, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((width - text_width) / 2, height - text_height - 30)

    shadowcolor = "black"
    draw.text((position[0]+2, position[1]+2), titulo, font=font, fill=shadowcolor)
    draw.text(position, titulo, font=font, fill="white")

    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.
