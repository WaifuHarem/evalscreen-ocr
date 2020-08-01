import unittest
import random
import json
import os

from core.render import FontRenderer
from ocr import OCR

from ffr.ffr_core import FfrCore
from ffr.ffr_img_processing import FfrImgProcessing
from ffr.ffr_txt_processing import FfrTxtProcessing



class TestFFR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.font_path = 'unit_tests/data/ffr/fonts/NoteSans/NotoSans-Bold.ttf'
        cls.results_path = 'unit_tests/data/ffr/results'

        if not os.path.isdir(cls.results_path):
            os.mkdir(cls.results_path)

    
    def gen_image(self, text_gen):
        text = text_gen()
        color = tuple( random.randint(0, 255) for _ in range(4) )
        font_size = random.randint(8, 42)
        
        img = FontRenderer.render_ttf(text, self.font_path, font_size, color)
        return text, color, font_size, img


    def test_ffr_date_info_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_ffr_player_info_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_map_title_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_map_info_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_amazing_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_perfect_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_good_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_average_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_miss_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_boo_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_aaa_equiv_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_raw_goods_detect(self):
        def text_gen():
            return f'Raw Goods: {round(random.random()*100, 2)}'

        # Test data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr detected data through text parser
            txt_data = FfrTxtProcessing.get_raw_goods_txt(' '.join(ocr_data['text']))
            ocr_text = txt_data['raw_goods']

            # Run generated text through text parser
            txt_data = FfrTxtProcessing.get_raw_goods_txt(text)
            gen_text = txt_data['raw_goods']
        
            # Compare and record result
            if gen_text == ocr_text:
                num_ok += 1
            else:
                fail_data.append({
                    'gen_text' : gen_text,
                    'ocr_text' : ocr_text,
                    'size'     : font_size,
                    'color'    : color,
                })

        with open(f'{self.results_path}/raw_goods.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        self.assertGreaterEqual(num_ok/total, 0.9)


    def test_combo_detect(self):
        # TODO: generate image
        # TODO: process image
        # TODO: process text
        # TODO: Compare result
        pass


    def test_ffr_detect(self):
        filename = 'unit_tests/data/ffr/ss/test1.png'
        _, data = FfrCore(filename).process()

        print(data)