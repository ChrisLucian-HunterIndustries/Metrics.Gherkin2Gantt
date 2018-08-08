import ImageDraw
import ImageFont
import ImageOps
from PIL import Image


def rotate_and_draw_date(img, x_position, row_y, current_day, color):
    font = ImageFont.truetype("arial.ttf", 14)
    txt = Image.new('L', (100, 25))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), current_day.__str__(), font=font, fill=255)
    w = txt.rotate(-90, expand=1)
    img.paste(ImageOps.colorize(w, (0, 0, 0), color), (x_position, row_y), w)
