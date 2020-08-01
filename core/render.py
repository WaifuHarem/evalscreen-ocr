import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2


class FontRenderer():

    @staticmethod
    def render_ttf(text, fontpath, text_size, color):
        num_text_lines = text.count('\n') + 1

        font = ImageFont.truetype(fontpath, text_size)

        # see https://stackoverflow.com/a/46220683/3256177
        ascent, descent = font.getmetrics()
        (width, _), (_, _) = font.font.getsize(text)
        height = num_text_lines*(ascent + descent)

        # Padding around text
        pad_x = 10
        pad_y = 10

        # Create new image
        img = Image.new('RGB', (width + pad_x*2, height + pad_y*2), (0, 0, 0))
        
        # Draw onto image
        draw = ImageDraw.Draw(img)
        draw.text((pad_x, pad_y), text, font=font, fill=color)

        return np.array(img)
