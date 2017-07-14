# -*- encoding: UTF-8 -*-
# In this document a CharacterRecognition object is defined and used for identifying language of words
# All names should be encoded with utf-8


# ------------------------------------
class CharacterRecognition(object):
    # def __init__(self):
    #     pass

    def is_chinese_char(self, uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    def is_number(self, uchar):
        """判断一个unicode是否是数字"""
        if u'\u0030' <= uchar <= u'\u0039':
            return True
        else:
            return False

    def is_alphabetical_char(self, uchar):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
            return True
        else:
            return False

    def is_other_char(self, uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (self.is_chinese_char(uchar) or self.is_number(uchar) or self.is_alphabetical_char(uchar)):
            return True
        else:
            return False

    def halfwidth_to_fullwidth(self, uchar):
        """半角转全角"""
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
            return uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        return chr(inside_code)

    def fullwidth_to_halfwidth(self, uchar):
        """全角转半角"""
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
            return uchar
        return chr(inside_code)

    def __string_full_to_half__(self, ustring):
        """把字符串全角转半角"""
        return "".join([self.fullwidth_to_halfwidth(uchar) for uchar in ustring])

    def uniform(self, ustring):
        """格式化字符串，完成全角转半角，大写转小写的工作"""
        return self.__string_full_to_half__(ustring).lower()
# ------------------------------------


# ------------------------------------
# ------------------------------------


# ------------------------------------


if __name__ == '__main__':
    import time
    start_time = time.time()
    # -----------------------------------
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration)//3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: %d h %d m %f s' % (hour, minutes, seconds))
