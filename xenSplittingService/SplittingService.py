# -*- encoding: UTF-8 -*-
# In this document firm name and remarks are segmented
# --------------------------
import os
import re
import jieba
from xenSplittingService.Toponym import Toponym
from xenSplittingService.ServiceComponents import BlackWhiteObject
from xenSplittingService.ServiceComponents import UnicodeStringRecognition
# --------------------------


# ------------------------------------
class ContentSplit(object):
    def __init__(self, data_path='data', user_data_path=None, enable_user_data=False):
        source_path = str(os.path.abspath(__file__))
        source_path = source_path.split(os.path.sep)
        while source_path[-1] != 'xenSplittingService':
            source_path.pop()
        while 'xenSplittingService' in source_path:
            source_path.remove('xenSplittingService')
        self.source_path = os.path.sep.join(source_path)
        self.running_path = os.getcwd()
        self.data_path = os.path.join(self.source_path, data_path)
        self.path_predefined = dict()
        self.path_userdefined = dict()
        self.checker = list()
        if user_data_path is not None:
            self.user_data_path = user_data_path
        else:
            self.user_data_path = self.running_path
        self.enable_user_data = enable_user_data
        self.__define_path_dict__()
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
        # --------
        self.ustring_checker = UnicodeStringRecognition()
        self.toponym_checker = Toponym(data_path=self.data_path)
        # --------
        self.keywords_predefined = dict()
        self.keywords_usrdefined = dict()
        self.__load_black_white_list__()
        # TODO: load partition expression
        # --------
        try:
            jieba.load_userdict(self.path_predefined['DeveloperDefined'])
        except FileNotFoundError:
            self.checker.append('File data' + str(os.path.sep) + 'DeveloperDefinedAdjustment.txt '
                                'does not exit, but this error does not affect service function that much')
        self.list_tag = ['package', 'user']

    def __define_path_dict__(self):
        self.path_predefined['DeveloperDefined'] = os.path.join(self.source_path, self.data_path,
                                                                'DeveloperDefinedAdjustment.txt')
        self.path_predefined['CompanyServiceTypeWhitelist'] = os.path.join(self.source_path, self.data_path,
                                                                           'PackageDefinedServiceTypeWhitelist.xlsx')
        self.path_predefined['CompanyTypeWhitelist'] = os.path.join(self.source_path, self.data_path,
                                                                    'PackageDefinedFirmTypeWhitelist.xlsx')
        self.path_predefined['CompanyKeywordBlacklist'] = os.path.join(self.source_path, self.data_path,
                                                                       'PackageDefinedKeywordBlacklist.xlsx')
        self.path_predefined['CompanyPartitionExpression'] = os.path.join(self.source_path, self.data_path,
                                                                          'PackageDefinedPartitionExpression.xlsx')
        if self.enable_user_data is True:
            self.path_userdefined['CompanyTypeWhitelist'] = \
                os.path.join(self.user_data_path, 'UserDefinedCompanyTypeWhitelist.xlsx')
            self.path_userdefined['CompanyServiceTypeWhitelist'] = \
                os.path.join(self.user_data_path, 'UserDefinedCompanyServiceTypeWhitelist.xlsx')
            self.path_userdefined['CompanyKeywordBlacklist'] = \
                os.path.join(self.user_data_path, 'UserDefinedCompanyKeywordBlacklist.xlsx')

    def __load_black_white_list__(self):
        self.keywords_predefined['CompanyServiceTypeWhitelist'] = \
            BlackWhiteObject(excel_path=self.path_predefined['CompanyServiceTypeWhitelist'])
        self.keywords_predefined['CompanyTypeWhitelist'] = \
            BlackWhiteObject(excel_path=self.path_predefined['CompanyTypeWhitelist'])
        self.keywords_predefined['CompanyKeywordBlacklist'] = \
            BlackWhiteObject(excel_path=self.path_predefined['CompanyKeywordBlacklist'])
        for word in self.keywords_predefined['CompanyTypeWhitelist'].tags():
            jieba.add_word(word, freq=int(50 * len(word)), tag='n')
        for word in self.keywords_predefined['CompanyServiceTypeWhitelist'].tags():
            jieba.add_word(word, freq=100, tag='n')
        for word in self.keywords_predefined['CompanyKeywordBlacklist'].tags():
            jieba.add_word(word, freq=100, tag='n')
        if self.enable_user_data is True:
            try:
                self.keywords_usrdefined['CompanyTypeWhitelist'] = \
                    BlackWhiteObject(excel_path=self.path_userdefined['CompanyTypeWhitelist'])
                self.keywords_usrdefined['CompanyServiceTypeWhitelist'] = \
                    BlackWhiteObject(excel_path=self.path_userdefined['CompanyServiceTypeWhitelist'])
                self.keywords_usrdefined['CompanyKeywordBlacklist'] = \
                    BlackWhiteObject(excel_path=self.path_userdefined['CompanyKeywordBlacklist'])
                for word in self.keywords_usrdefined['CompanyTypeWhitelist'].tags():
                    jieba.add_word(word, freq=int(50 * len(word)), tag='n')
                for word in self.keywords_usrdefined['CompanyServiceTypeWhitelist'].tags():
                    jieba.add_word(word, freq=100, tag='n')
                for word in self.keywords_usrdefined['CompanyKeywordBlacklist'].tags():
                    jieba.add_word(word, freq=100, tag='n')
            except:
                # TODO: initiate user defined files
                pass

    def __load_partition_expression__(self):
        pass

    def show_check_info(self):
        for info in self.checker:
            print(info)

    def add_company_type(self, new_company_type, force_add=False):
        pass

    def add_company_service_type(self, new_company_service_type, force_add=False):
        pass

    def add_blocked_company_keyword(self, new_block_word, force_add=False):
        pass

    def __show_checkers__(self):
        if len(self.checker) >= 1:
            print('Errors when launching Splitting Service: ')
            for err in self.checker:
                print('\t', err)
        else:
            pass


    def split_firm_name(self, name, enable_english_output=False, enable_digit_output=False):
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
    spliter = ContentSplit(data_path=os.path.join('xenSplittingService', 'data'))
    # -----------------------------------
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration) // 3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: {0:d} h {1:d} m {2:.2f} s'.format(hour, minutes, seconds))
