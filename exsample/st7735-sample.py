from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735

disp = ST7735.ST7735(
    port=0,
    cs=0,
    dc=24,
    backlight=19,
    rst=25,
    width=128,
    height=160,
    rotation=90,
    invert=False
)

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Load default font.
# font = ImageFont.load_default()
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)

# Write some text
draw.text((5, 5), "Hello World!", font=font, fill=(255, 255, 195))

# Write buffer to display hardware, must be called to make things visible on the
# display!
disp.display(img)