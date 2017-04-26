# -*- encoding: UTF-8 -*-
# In this document firm name and remarks are segmented
# --------------------------
import jieba
import re
import os
import csv
from xenSplittingService.china_landname import LandName
from xenSplittingService.service_configures import save_csv_2d, load_csv
# --------------------------


# ------------------------------------


# ------------------------------------
class ContentSplit(object):
    def __init__(self):
        self.path_pre_usr_identified_dict = os.path.join('..', 'data', 'pre_usr_identified_dict')
        self.path_usr_defined_company_type_whitelist = os.path.join('..', 'data', 'User_defined_company_type_whitelist.csv')
        self.path_usr_defined_company_service_type_whitelist = os.path.join('..', 'data',
                                                                       'User_defined_company_service_type_whitelist.csv')
        self.path_usr_defined_company_keyword_blacklist = os.path.join('..', 'data',
                                                                  'User_defined_company_keyword_blacklist.csv')
        self.path_company_service_type_whitelist = os.path.join('..', 'data', 'package_com_service_type_whitelist.csv')
        self.path_company_type_whitelist = os.path.join('..', 'data', 'package_com_type_whitelist.csv')
        self.path_company_keyword_blacklist = os.path.join('..', 'data', 'package_com_keyword_blacklist.csv')
        self.path_company_partition_expressions_csv = os.path.join('..', 'data', 'package_com_partition_expression.csv')

        self.landname_zh = LandName()
        self.reload_config_settings()

    def reload_config_settings(self):
        self.checker = list()
        self.__load_partition_expression__()
        print(self.partition_expression_dict)
        print(self.partition_expression_set)
        try:
            jieba.load_userdict(self.path_pre_usr_identified_dict)
        except FileNotFoundError:
            self.checker.append('File data/pre_usr_identified_dict does not exit, but this error '
                                'does not affect service function that much')
        try:
            self.company_partition_expression_dict = load_csv(self.path_company_partition_expressions_csv)
            print(self.company_partition_expression_dict)
        except:
            print('warning')
        # initial company_service_type_whitelist
        self.company_service_type_whitelist = \
            self.__load_config_list__(self.path_company_service_type_whitelist,
                                      self.path_usr_defined_company_service_type_whitelist,
                                      warning_pack_info='Whitelist data/package_com_service_type_whitelist.csv '
                                                        'can not be loaded correctly')
        # initial company type whitelist
        self.company_type_whitelist = \
            self.__load_config_list__(self.path_company_type_whitelist,
                                      self.path_usr_defined_company_type_whitelist,
                                      warning_pack_info='Whitelist data/package_com_type_whitelist.csv '
                                                        'can not be loaded correctly')
        # initial company_keyword_blacklist
        self.company_keyword_blacklist = \
            self.__load_config_list__(self.path_company_keyword_blacklist,
                                      self.path_usr_defined_company_keyword_blacklist,
                                      warning_pack_info='Blacklist data/package_com_keyword_blacklist.csv '
                                                        'can not be loaded correctly')
        # add name in company type white list to jieba dict so that they can be outputed.
        for __item__ in self.company_type_whitelist:
            jieba.add_word(__item__, freq=100, tag='n')
        self.__show_checkers__()

    def __load_config_list__(self, package_defined_csv, usr_defined_csv, warning_pack_info=''):
        __config_list__ = set()
        try:
            __file_content__ = load_csv(package_defined_csv)
            for __line__ in __file_content__:
                __config_list__.update(__line__)
        except:
            self.checker.append(warning_pack_info)
        try:
            __file_content__ = load_csv(usr_defined_csv)
            for __line__ in __file_content__:
                __config_list__.update(__line__)
        except FileNotFoundError:
            __file__ = open(usr_defined_csv, 'w', encoding='utf-8')
            __file__.close()
        __config_list__ = frozenset(__config_list__)
        return __config_list__

    # adding words to blacklists and whitelist
    def __add_into_list__(self, new_item, target_list, origin_list, typo_list=frozenset(), force_add=False):
        if new_item not in origin_list:
            if new_item not in typo_list or force_add:
                target_list.append(new_item)
                return True
            else:
                return False
        else:
            return False

    def __specified_adding_type__(self, new_term, target_set, file_path,
                                  typo_list=frozenset(), force_add_config=False):
        new_list = list()
        if type(new_term) is str:
            self.__add_into_list__(re.sub(r'\W', '', new_term), new_list, target_set,
                                   typo_list, force_add=force_add_config)
        elif type(new_term) is list:
            for __item__ in set(new_term):
                self.__add_into_list__(re.sub(r'\W', '', __item__), new_list, target_set,
                                       typo_list=typo_list, force_add=force_add_config)
        else:
            pass
        new_list = set(new_list)
        if len(new_list) > 0:
            try:
                __usr_defined__ = load_csv(file_path)
                for __line__ in __usr_defined__:
                    new_list.update(__line__)
            except FileNotFoundError:
                pass
            save_csv_2d(file_path, [[var] for var in new_list])
        new_list.update(target_set)
        return frozenset(new_list)

    def __load_partition_expression__(self):
        __csvfile__ = open(self.path_company_partition_expressions_csv, 'r', encoding='utf-8', newline='')
        __spam_writer__ = csv.reader(__csvfile__,
                                delimiter=',',
                                quotechar='"'
                                )
        __list_in_list__ = [var for var in __spam_writer__]
        __csvfile__.close()
        self.partition_expression_dict = dict()
        self.partition_expression_set = set()
        for __item__ in __list_in_list__:
            self.partition_expression_set.update(__item__)
            if len(__item__) > 1:
                for __word__ in range(1, len(__item__)):
                    self.partition_expression_dict[__item__[__word__]] = __item__[0]

    def add_company_type(self, new_company_type, force_add=False):
        self.company_type_whitelist = \
            self.__specified_adding_type__(new_company_type, self.company_type_whitelist,
                                           self.path_usr_defined_company_type_whitelist,
                                           typo_list=self.company_service_type_whitelist,
                                           force_add_config=force_add)

    def add_company_service_type(self, new_company_service_type, force_add=False):
        self.company_service_type_whitelist = \
            self.__specified_adding_type__(new_company_service_type,
                                           self.company_service_type_whitelist,
                                           self.path_usr_defined_company_service_type_whitelist,
                                           typo_list=self.company_type_whitelist,
                                           force_add_config=force_add)

    def add_blocked_company_keyword(self, new_block_word, force_add=False):
        self.company_keyword_blacklist = \
            self.__specified_adding_type__(new_block_word,
                                           self.company_keyword_blacklist,
                                           self.path_usr_defined_company_keyword_blacklist,
                                           force_add_config=force_add)

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
        # ---------------------------------------------------------- Identify company service types
        nameline.append('-')
        for item in namelist:
            if item in self.company_service_type_whitelist:
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
    print(splitter.company_type_whitelist, type(splitter.company_type_whitelist))
    print(splitter.company_service_type_whitelist, type(splitter.company_service_type_whitelist))
    print(splitter.company_keyword_blacklist, type(splitter.company_keyword_blacklist))
    splitter.add_company_type('test01', force_add=True)
    # splitter.add_company_type(['test02', 'test03'])
    splitter.add_company_service_type(['test02'])
    splitter.add_blocked_company_keyword('test01')
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
