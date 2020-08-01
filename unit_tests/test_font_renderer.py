import unittest
import random
import cv2

from core.render import FontRenderer



class TestFontRenderer(unittest.TestCase):

    def test_ttf_render(self):
        fontpath = 'unit_tests/data/ffr/fonts/NoteSans/NotoSans-Bold.ttf'

        for _ in range(15):
            text  = ''.join([ chr(random.randint(32, 126)) for char in range(22) ])
            color = tuple( random.randint(0, 255) for _ in range(4) )
            font_size = random.randint(8, 42)

            img = FontRenderer.render_ttf(text, fontpath, font_size, color)
            cv2.imshow('font', img)
            cv2.waitKey(500)
        
        cv2.destroyAllWindows()