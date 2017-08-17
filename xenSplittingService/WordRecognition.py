# -*- encoding: UTF-8 -*-
# In this document a CharacterRecognition object is defined and used for identifying language of words
# All names should be encoded with utf-8
# ------------------------------------
from xenSplittingService.DataStructure import CountingDict
# ------------------------------------


# ------------------------------------
class UnicodeCharacterRecognition(object):
    def __init__(self):
        self.language_list = ['english', 'chinese', 'digit', 'other']

    def check_uchar_type(self, uchar):
        if self.__is_chinese_char__(uchar):
            return 'chinese'
        elif self.__is_alphabetical_char__(uchar):
            return 'english'
        elif self.__is_digit__(uchar):
            return 'digit'
        else:
            return 'other'

    def __is_chinese_char__(self, uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    def __is_digit__(self, uchar):
        """判断一个unicode是否是数字"""
        if u'\u0030' <= uchar <= u'\u0039':
            return True
        else:
            return False

    def __is_alphabetical_char__(self, uchar):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
            return True
        else:
            return False

    def __is_other_char__(self, uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (self.__is_chinese_char__(uchar) or self.__is_digit__(uchar) or self.__is_alphabetical_char__(uchar)):
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
# ------------------------------------


# ------------------------------------
# ------------------------------------


# ------------------------------------
class UnicodeStringRecognition(UnicodeCharacterRecognition):
    def check_ustring_type(self, ustring):
        tag_dict = CountingDict()
        for char in ustring:
            tag_dict.count(self.check_uchar_type(char))
        return tag_dict.sort_by_weights(inverse=True)[0]

    def full_2_half(self, ustring):
        """把字符串全角转半角"""
        return ''.join([self.fullwidth_to_halfwidth(uchar) for uchar in ustring])

    def uniform(self, ustring):
        """格式化字符串，完成全角转半角，大写转小写的工作"""
        return self.full_2_half(ustring).lower()

    def identify_language(self, ustring):
        """Return the language of the string"""
        counter = dict()
        for lang in self.language_list:
            counter[lang] = 0
        for index_char in range(len(ustring)):
            ustring_type = self.check_uchar_type(ustring[index_char])
            counter[ustring_type] += 1
        possible_key = self.language_list[-1]
        better_value = 0
        for key, value in counter:
            if value > better_value:
                possible_key = key
        return possible_key
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
