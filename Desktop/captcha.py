from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


def rndChar():
    return chr(random.randint(65, 90))


def rndColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def main_capt():
    image = Image.new('RGB', (240, 60), (255, 255, 255))
    font = ImageFont.truetype('Ubuntu-Th.ttf', 50)
    draw = ImageDraw.Draw(image)

    for i in range(240):
        for j in range(60):
            draw.point((i, j), fill=rndColor())
    str_a = ''
    for i in range(4):
        alpha = rndChar()
        str_a += alpha
        draw.text((random.randint(20, 60) * i + random.randint(1, 20), random.randint(0, 10)), alpha, font=font,
                  fill=rndColor())

    image = image.filter(ImageFilter.BLUR)
    image.save('code.jpg', 'jpeg')
    return str_a


main_capt()
