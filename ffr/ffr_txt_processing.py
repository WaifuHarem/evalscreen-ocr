import re


class FfrTxtProcessing():

    @staticmethod
    def txt_to_float(txt):
        txt = txt.replace(',', '')
        txt = txt.replace('O', '0')
        txt = txt.replace('Q', '0')
        
        try: return float(txt)
        except ValueError:
            print('Unable to convert str to float; txt: ', txt)


    @staticmethod
    def get_date_info_txt(text):
        data = {
            'hour'   : None,
            'minute' : None,
            'second' : None,
            'ampm'   : None,
            'day'    : None,
            'month'  : None,
            'year'   : None,
        }

        regex = r"(\d+):(\d+):(\d+)(am|pm)\D*(\d+)/(\d+)/(\d+)"
        match = re.search(regex, text)
        if match:
            data['hour']   = FfrTxtProcessing.txt_to_float(match.group(1))
            data['minute'] = FfrTxtProcessing.txt_to_float(match.group(2))
            data['second'] = FfrTxtProcessing.txt_to_float(match.group(3))
            data['ampm']   = match.group(4)
            data['day']    = FfrTxtProcessing.txt_to_float(match.group(5))
            data['month']  = FfrTxtProcessing.txt_to_float(match.group(6))
            data['year']   = FfrTxtProcessing.txt_to_float(match.group(7))

        return data


    @staticmethod
    def get_player_info_txt(text):
        data = {
            'player' : None
        }

        regex = r"\[Lv\.\d+\]\s*(.*):"
        match = re.search(regex, text)
        if match:
            data['player'] = match.group(1)

        return data


    @staticmethod
    def get_map_title_txt(text):
        data = {
            'title' : None
        }

        regex = r"[\s]*[\S]*[\s]*(.*)"
        match = re.search(regex, text)
        if match:
            data['title'] = match.group(1)

        return data


    @staticmethod
    def get_map_info_txt(text):
        data = {
            'difficulty' : None,
            'length_min' : None,
            'length_sec' : None,
            'artist'     : None,
            'creator'    : None,
        }

        regex = r"Difficulty:\D*(\d+)\D*Length:\D*(\d+):(\d+)\D*Artist:([^-]+)\D*Stepfile by:([^-]+)"
        match = re.search(regex, text)
        if match:
            data['difficulty'] = FfrTxtProcessing.txt_to_float(match.group(1))
            data['length_min'] = FfrTxtProcessing.txt_to_float(match.group(2))
            data['length_sec'] = FfrTxtProcessing.txt_to_float(match.group(3))
            data['artist']     = match.group(4)
            data['creator']    = match.group(5)

        return data


    @staticmethod
    def get_amazing_txt(text):
        data = {
            'amazing_score' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['amazing_score'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_perfect_txt(text):
        data = {
            'perfect_score' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['perfect_score'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_good_txt(text):
        data = {
            'good_score' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['good_score'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_average_txt(text):
        data = {
            'average_score' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['average_score'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_miss_txt(text):
        data = {
            'miss_score' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['miss_score'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_boo_txt(text):
        data = {
            'boo_score' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['boo_score'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data

    
    @staticmethod
    def get_aaa_equiv_txt(text):
        data = {
            'AAA_equiv' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['AAA_equiv'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_raw_goods_txt(text):
        data = {
            'raw_goods' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['raw_goods'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data


    @staticmethod
    def get_combo_txt(text):
        data = {
            'combo' : None
        }

        regex = r":\s*(\S+)$"
        match = re.search(regex, text)
        if match:
            data['combo'] = FfrTxtProcessing.txt_to_float(match.group(1))

        return data