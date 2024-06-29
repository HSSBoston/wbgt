from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

display = InkyPHAT()
image = Image.new("P", (display.WIDTH, display.HEIGHT), display.BLACK)
display.set_image(image)
display.show()

