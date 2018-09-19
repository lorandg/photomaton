from PIL import Image, ImageDraw, ImageFont
import time
 
fnt = ImageFont.truetype('arial.ttf', 60)
 
for i in range(1,15) :
    img = Image.new('RGB', (1920, 1080), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((30,20), "%d"%i, font=fnt, fill=(255, 255, 0))
    img.save('../static/img/%d.jpg'%i)
    time.sleep(0.05)