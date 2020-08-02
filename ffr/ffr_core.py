import datetime
import numpy as np
import cv2
import re

from core.ocr import OCR
from ffr.ffr_img_processing import FfrImgProcessing
from ffr.ffr_txt_processing import FfrTxtProcessing



class FfrCore():

    # The game area w:h ratio
    ratio = 1.6254901960784313725490196078431

    # Constants to access rgb channels
    red   = 0
    green = 1
    blue  = 2
    
    def __init__(self, filename):
        self.__map_proc()
        self.__prepare_img(filename)


    def process_image(self):
        img_data = {}

        for key, img_func in self.img_proc.items():
            img_data[key] = img_func(self.img)

        return img_data


    def detect_text(self, img_data):
        ocr_data = {}

        for key, img in img_data.items():
            ocr_data[key] = OCR.detect_data(img)

        return ocr_data


    def process_text(self, ocr_data):
        txt_data = {}

        for proc_items, data_items in zip(self.txt_proc.items(), ocr_data.items()):
            proc_key, txt_func = proc_items
            ocr_key, data = data_items

            # This will happen only if there is a programming mistake
            if proc_key != ocr_key:
                raise Exception(f'procedure key != ocr key; proc_key = {proc_key}, ocr_key = {ocr_key}')

            txt_data.update(txt_func(' '.join(data['text'])))

        return txt_data


    def process(self):
        """
        data format:
        {
            'hour'          : float,
            'minute'        : float,
            'second'        : float,
            'ampm'          : str,
            'day'           : float,
            'month'         : float,
            'year'          : float,
            'player'        : str,
            'title'         : str,
            'difficulty'    : float,
            'length_min'    : float,
            'length_sec'    : float,
            'artist'        : str,
            'creator'       : str,
            'amazing_score' : float,
            'perfect_score' : float,
            'good_score'    : float,
            'average_score' : float,
            'miss_score'    : float,
            'boo_score'     : float,
            'AAA_equiv'     : float,
            'raw_goods'     : float,
            'combo'         : float,
        }
        """
        img_data = self.process_image()
        ocr_data = self.detect_text(img_data)
        txt_data = self.process_text(ocr_data)

        # Draw detection boundaries in the images
        for ocr_items, img_items in zip(ocr_data.items(), img_data.items()):
            ocr_key, ocr_item = ocr_items
            img_key, img_item = img_items

            # This will happen only if there is a programming mistake
            if img_key != ocr_key:
                raise Exception(f'image key != ocr key; img_key = {img_key}, ocr_key = {ocr_key}')

            FfrImgProcessing.draw_boundary(img_item, ocr_item)

        return img_data, txt_data


    def __prepare_img(self, filename):
        '''
        Loads and crops image to include just the game area
        '''
        
        # read the image and get the dimensions
        img = cv2.imread(filename)

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]
        channels = img.shape[2]

        # Crop to game area
        if width > height:
            new_width = FfrCore.ratio*height
            black_bar_width = (width - new_width)/2

            # If statement guard against window title bar
            if black_bar_width > 0:
                img = img[:, int(black_bar_width) : int(width - black_bar_width)]
        else:
            new_height = width/FfrCore.ratio
            black_bar_height = (height - new_height)/2

            # If statement just in case
            if black_bar_height > 0:
                img = img[int(black_bar_height) : int(height - black_bar_height), :]

        # height, width, number of channels in image
        height   = img.shape[0]
        width    = img.shape[1]
        channels = img.shape[2]

        # See if the window title bar needs to be cropped out
        if width > height:
            new_height = width/FfrCore.ratio
            title_bar_height = height - new_height
            img = img[int(title_bar_height):, :]

        # height, width, number of channels in image
        self.height   = img.shape[0]
        self.width    = img.shape[1]
        self.channels = img.shape[2]

        # Filter out unwanted background color
        r_treshold = (0 <= img[:, :, FfrCore.red]) & (img[:, :, FfrCore.red] <= 60)
        g_treshold = (0 <= img[:, :, FfrCore.green]) & (img[:, :, FfrCore.green] <= 60)
        b_treshold = (0 <= img[:, :, FfrCore.blue])  & (img[:, :, FfrCore.blue] <= 60)
        img[r_treshold & g_treshold & b_treshold] = 0

        self.img = img


    def __map_proc(self):
        self.img_proc = {}
        self.txt_proc = {}

        self.img_proc['data_info'],   self.txt_proc['data_info']   = FfrImgProcessing.get_date_info_img,   FfrTxtProcessing.get_date_info_txt       
        self.img_proc['player_info'], self.txt_proc['player_info'] = FfrImgProcessing.get_player_info_img, FfrTxtProcessing.get_player_info_txt       
        self.img_proc['map_title'],   self.txt_proc['map_title']   = FfrImgProcessing.get_map_title_img,   FfrTxtProcessing.get_map_title_txt     
        self.img_proc['map_info'],    self.txt_proc['map_info']    = FfrImgProcessing.get_map_info_img,    FfrTxtProcessing.get_map_info_txt      
        self.img_proc['amazing'],     self.txt_proc['amazing']     = FfrImgProcessing.get_amazing_img,     FfrTxtProcessing.get_amazing_txt      
        self.img_proc['perfect'],     self.txt_proc['perfect']     = FfrImgProcessing.get_perfect_img,     FfrTxtProcessing.get_perfect_txt      
        self.img_proc['good'],        self.txt_proc['good']        = FfrImgProcessing.get_good_img,        FfrTxtProcessing.get_good_txt   
        self.img_proc['average'],     self.txt_proc['average']     = FfrImgProcessing.get_average_img,     FfrTxtProcessing.get_average_txt     
        self.img_proc['miss'],        self.txt_proc['miss']        = FfrImgProcessing.get_miss_img,        FfrTxtProcessing.get_miss_txt   
        self.img_proc['boo'],         self.txt_proc['boo']         = FfrImgProcessing.get_boo_img,         FfrTxtProcessing.get_boo_txt   
        self.img_proc['aaa_equiv'],   self.txt_proc['aaa_equiv']   = FfrImgProcessing.get_aaa_equiv_img,   FfrTxtProcessing.get_aaa_equiv_txt      
        self.img_proc['raw_goods'],   self.txt_proc['raw_goods']   = FfrImgProcessing.get_raw_goods_img,   FfrTxtProcessing.get_raw_goods_txt      
        self.img_proc['combo'],       self.txt_proc['combo']       = FfrImgProcessing.get_combo_img,       FfrTxtProcessing.get_combo_txt      