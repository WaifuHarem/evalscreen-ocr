import unittest
import random
import json
import os

from core.render import FontRenderer
from core.ocr import OCR

from ffr.ffr_core import FfrCore
from ffr.ffr_img_processing import FfrImgProcessing
from ffr.ffr_txt_processing import FfrTxtProcessing



class TestFFR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.font_path = 'unit_tests/data/ffr/fonts/NoteSans/NotoSans-Bold.ttf'
        cls.results_path = 'unit_tests/data/ffr/results'
        cls.detection_rates = {}

        if not os.path.isdir(cls.results_path):
            os.mkdir(cls.results_path)


    @classmethod
    def tearDownClass(cls):
        with open(f'{cls.results_path}/detection_rates.txt', 'w') as f:
            f.write(json.dumps(cls.detection_rates, indent=4))

    
    def gen_image(self, text_gen):
        text = text_gen()
        color = (255, 255, 255, 255)
        font_size = random.randint(8, 42)
        
        img = FontRenderer.render_ttf(text, self.font_path, font_size, color)
        return text, color, font_size, img


    def test_ffr_date_info_detect(self):
        def text_gen():
            return f'{random.randint(0, 99)}:{random.randint(0, 99)}:{random.randint(0, 99)}{random.choice(["am", "pm"])}, {random.randint(0, 99)}/{random.randint(0, 99)}/{random.randint(2020, 2100)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_date_info_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_date_info_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })

                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/date_info.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['date_info'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_player_info_detect(self):
        def rand_text():
            return ''.join([ chr(random.randint(32, 126)) for char in range(12) ])

        def text_gen():
            return f'Results for [Lv. {random.randint(0, 999)}] {rand_text()}:'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_player_info_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_player_info_txt(' '.join(ocr_data['text']))
        
            all_ok = True

            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })

                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/player_info.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['player_info'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_map_title_detect(self):
        def rand_text():
            return ''.join([ chr(random.randint(32, 126)) for char in range(32) ])

        def text_gen():
            return rand_text()

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_map_title_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_map_title_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })

                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/map_title.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['map_title'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_map_info_detect(self):
        def rand_text():
            return ''.join([ chr(random.randint(32, 126)) for char in range(22) ])

        def text_gen():
            return f'Difficulty: {random.randint(0, 999)} - Length: {random.randint(0, 99)}:{random.randint(0, 99)} - Artist: {rand_text()} - Stepfile by: {rand_text()}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_map_info_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_map_info_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/map_info.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['map_info'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_amazing_detect(self):
        def text_gen():
            return f'Amazing: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_amazing_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_amazing_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/amazing_score.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['amazing_score'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_perfect_detect(self):
        def text_gen():
            return f'Perfect: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_perfect_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_perfect_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/perfect_score.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['perfect_score'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_good_detect(self):
        def text_gen():
            return f'Good: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_good_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_good_txt(' '.join(ocr_data['text']))
        
            all_ok = True
       
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/good_score.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['good_score'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_average_detect(self):
        def text_gen():
            return f'Average: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)      

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_average_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_average_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/average_score.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['average_score'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_miss_detect(self):
        def text_gen():
            return f'Miss: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_miss_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_miss_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/miss_score.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['miss_score'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_boo_detect(self):
        def text_gen():
            return f'Boo: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_boo_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_boo_txt(' '.join(ocr_data['text']))
        
            all_ok = True
        
            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/boo_score.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['boo_score'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_aaa_equiv_detect(self):
        def text_gen():
            return f'AAA Equivalency: {round(random.random()*100, 2)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_aaa_equiv_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_aaa_equiv_txt(' '.join(ocr_data['text']))
        
            all_ok = True

            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/AAA_equiv.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['AAA_equiv'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_raw_goods_detect(self):
        def text_gen():
            return f'Raw Goods: {round(random.random()*100, 2)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_raw_goods_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_raw_goods_txt(' '.join(ocr_data['text']))
        
            all_ok = True

            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/raw_goods.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['raw_goods'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_combo_detect(self):
        def text_gen():
            return f'Max Combo: {random.randint(0, 9999)}'

        # Results data
        total = 50
        num_ok = 0
        fail_data = []

        for _ in range(total):
            # Generate image
            text, color, font_size, img = self.gen_image(text_gen)
            ocr_data = OCR.detect_data(img)

            # Run ocr and generated data through text parser
            gen_txt_data = FfrTxtProcessing.get_combo_txt(text)
            ocr_txt_data = FfrTxtProcessing.get_combo_txt(' '.join(ocr_data['text']))
        
            all_ok = True

            # Compare and record result
            for gen_items, ocr_items in zip(gen_txt_data.items(), ocr_txt_data.items()):
                gen_key, gen_text = gen_items
                ocr_key, ocr_text = ocr_items

                # Sanity check
                self.assertEqual(gen_key, ocr_key)

                if gen_text != ocr_text:
                    fail_data.append({
                        'gen_text' : gen_txt_data,
                        'ocr_text' : ocr_txt_data,
                        'size'     : font_size,
                        'color'    : color,
                    })
                    
                    all_ok = False
                    break

            if all_ok:
                num_ok += 1

        with open(f'{self.results_path}/combo.txt', 'w') as f:
            f.write(json.dumps(fail_data, indent=4))

        detection_rate = num_ok/total
        self.detection_rates['combo'] = detection_rate
        self.assertGreaterEqual(detection_rate, 0.9)


    def test_ffr_detect(self):
        filename = 'unit_tests/data/ffr/ss/test1.png'
        _, data = FfrCore(filename).process()

        #print(data)