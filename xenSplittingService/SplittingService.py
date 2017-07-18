# -*- encoding: UTF-8 -*-
# In this document firm name and remarks are segmented
# --------------------------
import os
import re
import jieba
from xenSplittingService.Toponym import Toponym
from xenSplittingService.WordRecognition import UnicodeCharacterRecognition
from xenSplittingService.ServiceComponents import MultiList, ExcelFileWriter, load_excel
# --------------------------


# ------------------------------------
class ContentSplit(object):
    def __init__(self, data_path=os.path.join('data'), user_data_path=None):
        source_path = str(os.path.abspath(__file__))
        source_path = source_path.split(os.path.sep)
        while source_path[-1] != 'xenSplittingService':
            source_path.pop()
        while 'xenSplittingService' in source_path:
            source_path.remove('xenSplittingService')
        self.source_path = os.path.sep.join(source_path)
        self.running_path = os.getcwd()
        self.user_data_path = user_data_path    # TODO: check and modify user_data_path
        self.data_path = data_path
        self.path_predefined = dict()
        self.path_predefined['DeveloperDefined'] = os.path.join(self.source_path, self.data_path, 'DeveloperDefinedAdjustment.txt')
        self.path_predefined['CompanyServiceTypeWhitelist'] = os.path.join(self.source_path, self.data_path, 'package_com_service_type_whitelist.csv')
        self.path_predefined['CompanyTypeWhitelist'] = os.path.join(self.source_path, self.data_path, 'package_com_type_whitelist.csv')
        self.path_predefined['CompanyKeywordBlacklist'] = os.path.join(self.source_path, self.data_path, 'package_com_keyword_blacklist.csv')
        self.path_predefined['CompanyPartitionExpression'] = os.path.join(self.source_path, self.data_path, 'package_com_partition_expression.csv')
        self.path_userdefined = dict()
        self.path_userdefined['CompanyTypeWhitelist'] = os.path.join(self.running_path, 'User_defined_company_type_whitelist.csv')
        self.path_userdefined['CompanyServiceTypeWhitelist'] = os.path.join(self.running_path, 'User_defined_company_service_type_whitelist.csv')
        self.path_userdefined['CompanyKeywordBlacklist'] = os.path.join(self.running_path, 'User_defined_company_keyword_blacklist.csv')
        # --------
        self.path_pre_usr_identified_dict = None
        self.path_company_service_type_whitelist = None
        self.path_company_type_whitelist = None
        self.path_company_keyword_blacklist = None
        self.path_company_partition_expressions_csv = None
        # --------
        self.path_usr_defined_company_type_whitelist = None
        self.path_usr_defined_company_service_type_whitelist = None
        self.path_usr_defined_company_keyword_blacklist = None
        self.char_checker = UnicodeCharacterRecognition()
        self.land_name_checker = Toponym(data_path=self.data_path)
        self.checker = list()
        self.list_tag = ['package', 'user']
        self.load_checking_lists()

    def load_checking_lists(self):
        try:
            jieba.load_userdict(self.path_predefined['DeveloperDefined'])
        except FileNotFoundError:
            self.checker.append('File data' + str(os.path.sep) + 'DeveloperDefinedAdjustment.txt '
                                'does not exit, but this error does not affect service function that much')
            self.__load_partition_expression__()
            # initial company_service_type_whitelist
            self.company_service_type_whitelist = \
                self.__load_keyword_list__(self.path_company_service_type_whitelist,
                                           self.path_usr_defined_company_service_type_whitelist,
                                           warning_pack_info='Whitelist data/package_com_service_type_whitelist.csv '
                                                            'can not be loaded correctly')
            # initial company type whitelist
            self.company_type_whitelist = \
                self.__load_keyword_list__(self.path_company_type_whitelist,
                                           self.path_usr_defined_company_type_whitelist,
                                           warning_pack_info='Whitelist data/package_com_type_whitelist.csv '
                                                            'can not be loaded correctly')
            # initial company_keyword_blacklist
            self.company_keyword_blacklist = \
                self.__load_keyword_list__(self.path_company_keyword_blacklist,
                                           self.path_usr_defined_company_keyword_blacklist,
                                           warning_pack_info='Blacklist data/package_com_keyword_blacklist.csv '
                                                            'can not be loaded correctly')
        # add name in company type white list to jieba dict so that they can be outputed.
        for __item__ in self.company_type_whitelist:
            jieba.add_word(__item__, freq=int(50*len(__item__)), tag='n')
        for __item__ in self.company_service_type_whitelist:
            jieba.add_word(__item__, freq=100, tag='n')
        for __item__ in self.partition_expression_set:
            jieba.add_word(__item__, freq=100, tag='n')
        self.__show_checkers__()

    def __load_keyword_list__(self, package_defined_csv, usr_defined_csv=None, warning_pack_info=''):
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
        except TypeError:
            pass
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

    def is_eng_name(self, name, possi=0.6):
        name = re.sub(r'\W', "", name)
        count = 0
        for char in name:
            if self.__is_english_char(char) is True:
                count += 1
        if count/len(name) >= possi:
            return True
        else:
            return False

    def is_chi_name(self, name, possi=0.6):
        name = re.sub(r'\W', "", name)
        count = 0
        for char in name:
            if self.__is_chinese_char(char) is True:
                count += 1
        if count/len(name) >= possi:
            return True
        else:
            return False


    def split_firmname(self, name, enable_english_output=False, enable_digit_output=False):
        if self.is_chi_name(name, possi=0.6):
            return self.split_firmname_zh(name, enable_english_output)
        elif self.is_eng_name(name, possi=0.6):
            return self.split_firmname_en(name, enable_digit_output)
        else:
            return list()

    def split_firmname_zh(self, name, enable_english=False, enable_digit=True):
        item_text = jieba.cut(str(name))
        namelist = list(item_text)
        # ---------------------------------------------------------- cleanning
        for index in range(len(namelist)):
            namelist[index] = re.sub(r'\W', "", namelist[index])
        if enable_english is False:
            for index in range(len(namelist)):
                namelist[index] = re.sub(r'[a-zA-Z]', '', namelist[index])
        if enable_digit is False:
            for index in range(len(namelist)):
                namelist[index] = re.sub(r'[0123456789]', '', namelist[index])
        while '' in namelist:
            namelist.remove('')
        locationchecker = self.landname_zh
        nameline = list()
        # ---------------------------------------------------------- derive locationchecker
        nameline.append('-')
        if not self.__any_partition_in__(namelist):
            if locationchecker.check_location_name(namelist[0]) is not None:
                nameline[0] = locationchecker.check_location_name(namelist[0])
                del namelist[0]
            else:
                if '中国' not in namelist:
                    if '(' in namelist and ')' in namelist:
                        aindex = namelist.index('(')
                        bindex = namelist.index(')')
                        if bindex - aindex > 1:
                            for index in range(aindex+1, bindex, 1):
                                if locationchecker.check_location_name(namelist[index]) is not None:
                                    nameline[0] = locationchecker.check_location_name(namelist[index])
                                    del namelist[index]
                                    break
                    else:
                        if '(' in namelist:
                            aindex = namelist.index('(')
                            for index in range(aindex + 1, len(namelist), 1):
                                if locationchecker.check_location_name(namelist[index]) is not None:
                                    nameline[0] = locationchecker.check_location_name(namelist[index])
                                    del namelist[index]
                                    break
                        else:
                            for index in range(1, len(namelist), 1):
                                if locationchecker.check_location_name(namelist[index]) is not None:
                                    nameline[0] = locationchecker.check_location_name(namelist[index])
                                    del namelist[index]
                                    break
                else:
                    namelist.remove('中国')
                    for index in range(1, len(namelist)):
                        if locationchecker.check_location_name(namelist[index]) is not None:
                            nameline[0] = locationchecker.check_location_name(namelist[index])
                            del namelist[index]
                            break
        else:
            tailindex = self.__index_partition_in__(namelist)
            if tailindex >= 1:
                formerindex = 0
                for i in range(tailindex-1, -1, -1):
                    if '公司' in namelist[i]:
                        formerindex = i
                for j in range(formerindex+1, tailindex, 1):
                    if locationchecker.check_location_name(namelist[j]) is not None:
                        nameline[0] = locationchecker.check_location_name(namelist[j])
                        del namelist[j]
                        break
                if nameline[0] == '-':
                    if locationchecker.check_location_name(namelist[0]) is not None:
                        nameline[0] = locationchecker.check_location_name(namelist[0])
                        del namelist[0]
                    else:
                        for index in range(1, formerindex, 1):
                            if locationchecker.check_location_name(namelist[index]) is not None:
                                nameline[0] = locationchecker.check_location_name(namelist[index])
                                del namelist[index]
                                break
            else:
                if locationchecker.check_location_name(namelist[0]) is not None:
                    nameline[0] = locationchecker.check_location_name(namelist[0])
                    del namelist[0]
        # ---------------------------------------------------------- Identify company types
        nameline.append('-')
        if len(set(self.pre_defined_company_type) & set(namelist)) > 0:
            for index in range(len(self.pre_defined_company_type)):
                if self.pre_defined_company_type[index] in namelist:
                    nameline[1] = self.pre_defined_company_type[index]
                    namelist.remove(self.pre_defined_company_type[index])
        else:
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
            if item not in self.company_keyword_blacklist:
                nameline.append(item)
        return nameline

    def __any_partition_in__(self, list_obj):
        for __partition__ in self.partition_expression_set:
            if __partition__ in list_obj:
                return True
        return False

    def __index_partition_in__(self, list_obj):
        for __partition__ in self.partition_expression_set:
            if __partition__ in list_obj:
                return list_obj.index(__partition__)
        return 0

    def split_firmname_en(self, name, allow_digit=False):
        item_text = list(jieba.cut(str(name)))
        for __index__ in range(len(item_text)):
            item_text[__index__] = re.sub(r'\W', '', item_text[__index__])
        if allow_digit:
            for __index__ in range(len(item_text)):
                item_text[__index__] = re.sub(r'\d', '', item_text[__index__])
        while '' in item_text:
            item_text.remove('')
        name_line = list()
        # ---------------------------------------- derive location
        name_line.append('-')
        # ---------------------------------------- derive company type
        name_line.append('-')
        # ---------------------------------------- derive company service type
        name_line.append('-')
        for __item__ in item_text:
            name_line.append(__item__)
        return name_line


    def split_msg(self, content, enable_english_output=True, enable_digit_output=True):
        item_text = jieba.cut(str(content))
        item_text = list(item_text)
        for i in range(len(item_text)):
            item_text[i] = re.sub(r'\W', "", item_text[i])
            if enable_english_output is False:
                item_text[i] = re.sub(r'[a-zA-Z]', '', item_text[i])
            if enable_digit_output is False:
                item_text[i] = re.sub(r'[0123456789]', '', item_text[i])
        while '' in item_text:
            item_text.remove('')
        new_list = list()
        for index in range(len(item_text)):
            if item_text[index] not in self.company_keyword_blacklist:
                new_list.append(item_text[index])
        return new_list

    def split(self, content, enable_english_output=True, enable_digit_output=True):
        item_text = jieba.cut(str(content))
        item_text = list(item_text)
        for i in range(len(item_text)):
            item_text[i] = re.sub(r'\W', "", item_text[i])
            if enable_english_output is False:
                item_text[i] = re.sub(r'[a-zA-Z]', '', item_text[i])
            if enable_digit_output is False:
                item_text[i] = re.sub(r'[0123456789]', '', item_text[i])
        while '' in item_text:
            item_text.remove('')
        new_list = list()
        for index in range(len(item_text)):
            if item_text[index] not in self.company_keyword_blacklist:
                new_list.append(item_text[index])
        return new_list


if __name__ == '__main__':
    import time
    start_time = time.time()
    # -----------------------------------
    # -----------------------------------
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration)//3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: %d h %d m %f s' % (hour, minutes, seconds))
