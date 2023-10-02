import datetime
import random

from PIL import Image, ImageDraw, ImageFont


def generate_code():
    first_digit = str(random.randint(1, 9))
    date = datetime.date.today().strftime('%d%m%Y')
    last_digit = ''.join([str(random.randint(0, 9)) for i in range(6)])
    return first_digit + date + last_digit


def draw_code(code: str, path: str):
    im = Image.new('RGB', (920, 600), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    MM_PIXEL = 3.793627 * 10
    start_x = round(3.56 * MM_PIXEL)
    h = 0
    long_lines = [start_x - (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL))]
    sered = [len(code) / 2, len(code) / 2 + 1] if len(code) % 2 == 0 else [round(len(code) / 2)]
    draw.line((start_x - (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)) * 2, 50, start_x
               - (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)) * 2, 550), fill='black',
              width=round(1 * 0.15 * MM_PIXEL))
    draw.line((start_x - (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)), 50,
               start_x - (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)), 550), fill='black',
              width=round(1 * 0.15 * MM_PIXEL))
    for i in code:
        if h in sered:
            draw.line((start_x, 50, start_x, 550), fill='black',
                      width=round(1 * 0.15 * MM_PIXEL))
            start_x += round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)
            long_lines.append(start_x)
        if int(i) != 0:
            draw.line((start_x, 50, start_x, 500), fill='black',
                      width=round(int(i) * 0.15 * MM_PIXEL))
            start_x += round(0.2 * MM_PIXEL) + round(int(i) * 0.15 * MM_PIXEL)
        else:
            start_x += round(1.35 * MM_PIXEL)
        h += 1
    draw.line((start_x + (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)) * 2, 50, start_x
               + (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)) * 2, 550), fill='black',
              width=round(1 * 0.15 * MM_PIXEL))
    long_lines.append(start_x + (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)))
    draw.line((start_x + (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)), 50,
               start_x + (round(0.2 * MM_PIXEL) + round(1 * 0.15 * MM_PIXEL)), 550), fill='black',
              width=round(1 * 0.15 * MM_PIXEL))
    font = ImageFont.truetype('Ubuntu-Th.ttf', 30)
    h1 = 1
    for i in code:
        if True not in [True if i2 - 30 <= long_lines[0] + 30 * h1 < i2 + 30 else False for i2 in long_lines]:
            draw.text((long_lines[0] + 30 * h1, 520), i, font=font, fill=(0, 0, 0))
        else:
            while True in [True if i2 - 30 <= long_lines[0] + 30 * h1 < i2 + 30 else False for i2 in long_lines]:
                long_lines[0] += 5
            draw.text((long_lines[0] + 30 * h1, 520), i, font=font, fill=(0, 0, 0))
        h1 += 1
    im.save(path + '/barcode.pdf')
