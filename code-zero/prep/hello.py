from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

display = InkyPHAT("red")

image = Image.new("P", (display.WIDTH, display.HEIGHT), display.WHITE)
draw = ImageDraw.Draw(image)

# font = ImageFont.load_default()
font = ImageFont.truetype("JetBrainsMono-Regular.ttf", 32) 

draw.text((0, 0), "Hello!", display.RED, font=font)
display.set_image(image)
display.show()


