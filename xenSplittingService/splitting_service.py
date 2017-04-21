# -*- encoding: UTF-8 -*-
# In this document firm name and remarks are segmented
# --------------------------
import jieba
import re
from xenSplittingService.china_landname import LandName
from xenSplittingService.service_configures import load_csv, save_csv_2d
# --------------------------


# ------------------------------------


# ------------------------------------
class ContentSplit(object):
    def __init__(self):
        self.landname_zh = LandName()
        self.reload_config_settings()

    def reload_config_settings(self):
        self.checker = list()
        try:
            jieba.load_userdict("../data/pre_usr_identified_dict")
        except FileNotFoundError:
            self.checker.append('File data/pre_usr_identified_dict does not exit, but this error '
                                'does not affect service function that much')
        # initial company_service_type_whitelist
        self.company_service_type_whitelist = set()
        try:
            __file_content__ = load_csv('../data/Company ServiceType Whitelist.csv')
            for __line__ in __file_content__:
                self.company_service_type_whitelist.update(__line__)
            self.company_service_type_whitelist = frozenset(self.company_service_type_whitelist)
        except:
            self.checker.append('Whitelist data/Company ServiceType Whitelist.csv can not be loaded correctly')
        # initial company_type_whitelist
        self.company_type_whitelist = set()
        try:
            __file_content__ = load_csv('../data/Company Type Whitelist.csv')
            for __line__ in __file_content__:
                self.company_type_whitelist.update(__line__)
            self.company_type_whitelist = frozenset(self.company_type_whitelist)
        except:
            self.checker.append('Whitelist data/Company Type Whitelist.csv can not be loaded correctly')
        self.company_keyword_blacklist = set()
        try:
            __file_content__ = load_csv('../data/Company KeyWord Blacklist.csv')
            for __line__ in __file_content__:
                self.company_keyword_blacklist.update(__line__)
            self.company_keyword_blacklist = frozenset(self.company_keyword_blacklist)
        except:
            self.checker.append('Blacklist data/Company KeyWord Blacklist.csv can not be loaded correctly')
        for __item__ in self.company_type_whitelist:
            jieba.add_word(__item__, freq=100, tag='n')
        self.__show_checkers__()

    def __add_into_list__(self, new_item, target_list, typo_list=frozenset(), force_add=False):
        if new_item not in target_list:
            if new_item not in typo_list or force_add:
                target_list.append(new_item)
                return True
            else:
                return False
        else:
            return False

    def add_company_type(self, new_company_type, force_add = False):
        if type(new_company_type) == str:
            added_company_type = re.sub(r'\W', '', new_company_type)
            new_list = list(self.company_type_whitelist)
            self.__add_into_list__(added_company_type, new_list,
                                   self.company_service_type_whitelist, force_add=force_add)
            if len(new_list) > len(self.company_type_whitelist):
                save_csv_2d('../data/Company Type Whitelist.csv', [[var] for var in new_list])
                self.company_type_whitelist = frozenset(new_list)
        elif type(new_company_type) == list:
            new_list = list(self.company_type_whitelist)
            for item in set(new_company_type):
                self.__add_into_list__(re.sub(r'\W', '', item), new_list,
                                       self.company_service_type_whitelist, force_add=force_add)
            if len(new_list) > len(self.company_type_whitelist):
                save_csv_2d('../data/Company Type Whitelist.csv', [[var] for var in new_list])
                self.company_type_whitelist = frozenset(new_list)
        else:
            pass


    def __show_checkers__(self):
        if len(self.checker) >= 1:
            print('Errors when launching Splitting Service: ')
            for err in self.checker:
                print('\t', err)
        else:
            pass

    def is_eng_name(self, name):
        name = re.sub(r'\W', "", name)
        count = 0
        for char in name:
            if self.__is_english_char(char) == 1:
                count += 1
        if count/len(name) >= 0.6:
            return 1
        else:
            return 0

    def is_chi_name(self, name):
        name = re.sub(r'\W', "", name)
        count = 0
        for char in name:
            if self.__is_chinese_char(char) == 1:
                count += 1
        if count/len(name) >= 0.6:
            return 1
        else:
            return 0

    def __is_english_char(self, uchar):
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False

    def __is_chinese_char(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    def split_firmname(self, name):
        if self.is_chi_name(name):
            return ' '.join(self.split_firmname_zh(name))
        else:
            return ''

    def split_firmname_zh(self, name):
        item_text = jieba.cut(str(name))
        namelist = list(item_text)
        while '\u3000' in namelist:
            namelist.remove('\u3000')
        locationchecker = self.landname_zh
        nameline = []
        # ---------------------------------------------------------- derive locationchecker
        if '分公司' not in namelist:
            if locationchecker.check_landname(namelist[0]) != None:
                nameline.append(locationchecker.check_landname(namelist[0]))
                del namelist[0]
            else:
                if '中国' not in namelist:
                    if '(' in namelist and ')' in namelist:
                        aindex = namelist.index('(')
                        bindex = namelist.index(')')
                        if bindex - aindex > 1:
                            for index in range(aindex+1, bindex, 1):
                                if len(nameline) == 0:
                                    if locationchecker.check_landname(namelist[index]) != None:
                                        nameline.append(locationchecker.check_landname(namelist[index]))
                                        del namelist[index]
                    else:
                        if '(' in namelist:
                            aindex = namelist.index('(')
                            for index in range(aindex + 1, len(namelist), 1):
                                if len(nameline) == 0:
                                    if locationchecker.check_landname(namelist[index]) != None:
                                        nameline.append(locationchecker.check_landname(namelist[index]))
                                        del namelist[index]
                        else:
                            for index in range(1, len(namelist), 1):
                                if len(nameline) == 0:
                                    if locationchecker.check_landname(namelist[index]) != None:
                                        nameline.append(locationchecker.check_landname(namelist[index]))
                                        del namelist[index]
                            if len(nameline) == 0:
                                nameline.append('-')
                            pass    # no locationchecker
                    if len(nameline) == 0:
                        nameline.append('-')
                else:
                    namelist.remove('中国')
                    for index in range(len(namelist)):
                        if len(nameline) == 0:
                            if locationchecker.check_landname(namelist[index]) != None:
                                nameline.append(locationchecker.check_landname(namelist[index]))
                                del namelist[index]
                    if len(nameline) == 0:
                        nameline.append('-')
        else:
            tailindex = namelist.index('分公司')
            if tailindex >= 1:
                formerindex = 0
                for i in range(tailindex-1, -1, -1):
                    if '公司' in namelist[i]:
                        formerindex = i
                for j in range(formerindex+1, tailindex, 1):
                    if locationchecker.check_landname(namelist[j]) is not None:
                        nameline.append(locationchecker.check_landname(namelist[j]))
                        del namelist[j]
                if len(nameline) == 0:
                    if locationchecker.check_landname(namelist[0]) is not None:
                        nameline.append(locationchecker.check_landname(namelist[0]))
                        del namelist[0]
                    else:
                        for index in range(1, formerindex, 1):
                            if len(nameline) == 0:
                                if locationchecker.check_landname(namelist[index]) is not None:
                                    nameline.append(locationchecker.check_landname(namelist[index]))
                                    del namelist[index]
                if len(nameline) == 0:
                    nameline.append('-')
            else:
                if len(nameline) == 0:
                    if locationchecker.check_landname(namelist[0]) is not None:
                        nameline.append(locationchecker.check_landname(namelist[0]))
                        del namelist[0]
                if len(nameline) == 0:
                    nameline.append('-')
        # ---------------------------------------------------------- cleanning
        for i in range(len(namelist)):
            namelist[i] = re.sub(r'\W', "", namelist[i])
        while '' in namelist:
            namelist.remove('')
        # ---------------------------------------------------------- Identify company types
        nameline.append('-')
        for item in namelist:
            if item in self.company_type_whitelist:
                nameline[1] = item
                namelist.remove(item)
        # ---------------------------------------------------------- merging
        indexlist = list()
        skiplist = list()
        for item in namelist:
            if len(item) == 1:
                indexlist.append(namelist.index(item))
        for i in range(len(indexlist)):
            if i not in skiplist:
                content = namelist[indexlist[i]]
                for j in range(i+1, len(indexlist), 1):
                    if j == i + indexlist[j] - indexlist[i]:
                        content += namelist[indexlist[j]]
                        skiplist.append(j)
                namelist[indexlist[i]] = content
        skiplist.reverse()
        for item in skiplist:
            del namelist[indexlist[item]]
        # ---------------------------------------------------------- appending last items
        for item in namelist:
            nameline.append(item)
        return nameline

    def split_msg(self, content):
        item_text = jieba.cut(str(content))
        item_text = list(item_text)
        for i in range(len(item_text)):
            item_text[i] = re.sub(r'\W', "", item_text[i])
        while '' in item_text:
            item_text.remove('')
        return ' '.join(item_text)

    def split(self, content):
        item_text = jieba.cut(str(content))
        item_text = list(item_text)
        for i in range(len(item_text)):
            item_text[i] = re.sub(r'\W', "", item_text[i])
        while '' in item_text:
            item_text.remove('')
        return ' '.join(item_text)


if __name__ == '__main__':
    import time
    start_time = time.time()
    # -----------------------------------
    splitter = ContentSplit()
    # splitter.add_company_type('test01')
    # splitter.add_company_type(['test02', 'test03'])
    print(splitter.split('无锡市外服人力资源有限公司'))
    print(splitter.split_firmname('无锡市外服人力资源有限公司'))
    # -----------------------------------
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration)//3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: %d h %d m %f s' % (hour, minutes, seconds))
