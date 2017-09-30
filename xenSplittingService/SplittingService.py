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
        self.keywords_predefined['CompanyPartitionExpression'] = \
            BlackWhiteObject(excel_path=self.path_predefined['CompanyPartitionExpression'])
        for word in self.keywords_predefined['CompanyTypeWhitelist'].tags():
            jieba.add_word(word, freq=int(50 * len(word)), tag='n')
        for word in self.keywords_predefined['CompanyServiceTypeWhitelist'].tags():
            jieba.add_word(word, freq=100, tag='n')
        for word in self.keywords_predefined['CompanyKeywordBlacklist'].tags():
            jieba.add_word(word, freq=100, tag='n')
        for word in self.keywords_predefined['CompanyPartitionExpression'].tags():
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
            except FileExistsError:
                # TODO: initiate user defined files
                pass

    def show_check_info(self):
        for info in self.checker:
            print(info)

    def __show_checkers__(self):
        if len(self.checker) >= 1:
            print('Errors when launching Splitting Service: ')
            for err in self.checker:
                print('\t', err)

    def __identify_firm_toponym__(self, words_list: list):
        for index in range(len(words_list)):
            word = words_list[index]
            if self.toponym_checker.check_location_name(name=word):
                del words_list[index]
                return word
        return '-'

    def __identify_firm_type__(self, words_list: list):
        for index in range(len(words_list)):
            word = words_list[index]
            if self.keywords_predefined['CompanyTypeWhitelist'].contain(word):
                del words_list[index]
                return word
        return '-'

    def __identify_firm_service_type__(self, words_list: list):
        for index in range(len(words_list)):
            word = words_list[index]
            if self.keywords_predefined['CompanyServiceTypeWhitelist'].contain(word):
                del words_list[index]
                return word
        return '-'

    def split_firm_name(self, name: str, **kwargs):
        name_list = self.split(name, **kwargs)
        result_line = list()
        result_line.append(self.__identify_firm_toponym__(words_list=name_list))
        result_line.append(self.__identify_firm_type__(words_list=name_list))
        result_line.append(self.__identify_firm_service_type__(words_list=name_list))
        for word in name_list:
            if not self.keywords_predefined['CompanyKeywordBlacklist'].contain(word):
                result_line.append(word)
        return result_line

    def split_msg(self, message: str, **kwargs):
        text_list = self.split(message, **kwargs)
        result_list = list()
        for word in text_list:
            if not self.keywords_predefined['CompanyKeywordBlacklist'].contain(word):
                result_list.append(word)
        return result_list

    def split(self, string: str, **kwargs):
        result_list = list(jieba.cut(re.sub(r'\W', ' ', self.ustring_checker.full_2_half(ustring=string))))
        for index in range(len(result_list)):
            result_list[index] = re.sub(r' ', '', result_list[index])
        for key in kwargs:
            key_str = str(key).split('_')
            if len(key_str) != 2:
                raise ValueError('ContentSplit.split_firm_name: command {0:s} is not legal'.format(str(key)))
            else:
                if key_str[1] in self.ustring_checker.language_base and key_str[0] == 'unable':
                    if key_str[1] == 'english':
                        for index in range(len(result_list)):
                            result_list[index] = re.sub(r'[a-zA-Z]', '', result_list[index])
                    elif key_str[1] == 'chinese':
                        pass
                        # TODO: finishing replacing chinese
                    else:
                        for index in range(len(result_list)):
                            result_list[index] = re.sub(r'[0123456789]', '', result_list[index])
                else:
                    raise ValueError('ContentSplit.split_firm_name: command {0:s} is not legal'.format(str(key)))
        while '' in result_list:
            result_list.remove('')
        return result_list


if __name__ == '__main__':
    import time
    start_time = time.time()
    # -----------------------------------
    import json
    spliter = ContentSplit(data_path=os.path.join('xenSplittingService', 'data'))
    com = json.load(open(os.path.join('..', 'data', 'com.json'), 'r'))
    print(com['RECORDS'])
    for record in com['RECORDS']:
        company_name = record['customer_name']
        spliited_list = spliter.split_firm_name(company_name, unable_digit=True, unable_english=True)
        print(company_name, '\t', spliited_list[2], spliited_list[3:])
        time.sleep(0.5)
    spliter.__show_checkers__()
    print(spliter.split_firm_name('无锡市外服人力资源集团有限公司', unable_english=True))
    # print(spliter.split_firmname("CNY 4,900-MERES MEDICAL CONSULTING CO.,LTD"))
    print(spliter.split_msg("CNY 4,900-MERES MEDICAL CONSULTING CO.,LTD", unable_digit=True, unable_english=True))
    # print(spliter.split_firmname('无锡市外服人力资源集团有限公司', enable_english_output=True))
    # -----------------------------------
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration) // 3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: {0:d} h {1:d} m {2:.2f} s'.format(hour, minutes, seconds))
