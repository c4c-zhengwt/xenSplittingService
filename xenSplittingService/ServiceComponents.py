# -*- encoding: UTF-8 -*-
# --------------------------------------------------------
import pandas as pd

from xenSplittingService.DataStructure import CountingDict


class UnicodeCharacterRecognition(object):
    def __init__(self):
        self.language_base = {
            'english': 0,
            'chinese': 1,
            'digit': 2,
            'other': 99,
        }

    def check_uchar_type(self, uchar):
        if self.__is_chinese_char__(uchar):
            return 'chinese'
        elif self.__is_alphabetical_char__(uchar):
            return 'english'
        elif self.__is_digit__(uchar):
            return 'digit'
        else:
            return 'other'

    @staticmethod
    def __is_chinese_char__(uchar):
        if u'\u4e00' <= uchar and uchar <= u'\u9fa5':
            return True
        else:
            return False

    @staticmethod
    def __is_digit__(uchar):
        """判断一个unicode是否是数字"""
        if u'\u0030' <= uchar and uchar <= u'\u0039':
            return True
        else:
            return False

    @staticmethod
    def __is_alphabetical_char__(uchar):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= uchar and uchar <= u'\u005a') or (u'\u0061' <= uchar and uchar <= u'\u007a'):
            return True
        else:
            return False

    def __is_other_char__(self, uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (self.__is_chinese_char__(uchar) or self.__is_digit__(uchar) or self.__is_alphabetical_char__(uchar)):
            return True
        else:
            return False

    @staticmethod
    def halfwidth_to_fullwidth(uchar):
        """半角转全角"""
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
            return uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        return chr(inside_code)

    @staticmethod
    def fullwidth_to_halfwidth(uchar):
        """全角转半角"""
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
            return uchar
        return chr(inside_code)


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
        for lang in self.language_base:
            counter[lang] = 0
        for index_char in range(len(ustring)):
            ustring_type = self.check_uchar_type(ustring[index_char])
            counter[ustring_type] += 1
        possible_key = 'other'
        better_value = 0
        for key, value in counter:
            if value > better_value:
                possible_key = key
        return possible_key


def load_excel(path, sheetname=0, header=0, skiprows=None, skip_footer=0, index_col=None, names=None,
               parse_cols=None, parse_dates=False, date_parser=None, na_values=None, thousands=None,
               convert_float=True, has_index_names=None, converters=None, dtype=None, true_values=None,
               false_values=None, engine=None, squeeze=False):
    """Use pandas.read_excel to load excel files"""
    return pd.read_excel(path, sheetname=sheetname, header=header, skiprows=skiprows, skip_footer=skip_footer,
                         index_col=index_col, names=names, parse_cols=parse_cols, parse_dates=parse_dates,
                         date_parser=date_parser, na_values=na_values, thousands=thousands, convert_float=convert_float,
                         has_index_names=has_index_names, converters=converters, dtype=dtype, true_values=true_values,
                         false_values=false_values, engine=engine, squeeze=squeeze)


class ExcelFileWriter(object):
    def __init__(self, path: str, engine='openpyxl'):
        self.writer = pd.ExcelWriter(path=path, engine=engine)

    def append_sheet(self, content: pd.DataFrame, sheet_name='Sheet1', na_rep=str(), float_format=None,
                     columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, merge_cells=True,
                     encoding=None, inf_rep='inf', verbose=True, freeze_panes=None):
        content.to_excel(excel_writer=self.writer, sheet_name=sheet_name, na_rep=na_rep, float_format=float_format,
                         columns=columns, header=header, index=index, index_label=index_label, startrow=startrow,
                         startcol=startcol, merge_cells=merge_cells, encoding=encoding, inf_rep=inf_rep,
                         verbose=verbose, freeze_panes=freeze_panes)

    def save(self):
        self.writer.save()

    def finish(self):
        self.writer.save()
        self.writer.close()
        del self


class ExcelObject(object):
    """
    ExcelTable
    """
    def __init__(self, excel_path: str,
                 header=0, skiprows=None, skip_footer=0, index_col=None, names=None,
                 parse_cols=None, parse_dates=False, date_parser=None, na_values=None, thousands=None,
                 convert_float=True, has_index_names=None, converters=None, dtype=None, true_values=None,
                 false_values=None, engine=None, squeeze=False
                 ):
        self.excel_file_path = excel_path
        self.language_list = ('chinese',)
        self.sheetname2language_dict = dict()
        self.language2sheetname_dict = dict()
        self.__initiate_words_transformation_dict__()
        self.excel_file = dict()
        for language in self.language_list:
            self.excel_file[language] = pd.read_excel(excel_path, sheetname=self.language2sheetname_dict[language],
                                                      header=header, skiprows=skiprows, skip_footer=skip_footer,
                                                      index_col=index_col, names=names, parse_cols=parse_cols,
                                                      parse_dates=parse_dates, date_parser=date_parser,
                                                      na_values=na_values, thousands=thousands,
                                                      convert_float=convert_float, has_index_names=has_index_names,
                                                      converters=converters, dtype=dtype, true_values=true_values,
                                                      false_values=false_values, engine=engine, squeeze=squeeze)
        self.data_list_for_search = dict()
        self.__initiate_list_for_search__()
        self.data_belongings_for_search = dict()
        self.__initiate_belongings_for_search__()

    def __initiate_words_transformation_dict__(self):
        raise NameError('ExcelObject.__initiate_words_transformation_dict__: method not defined')

    def __initiate_list_for_search__(self):
        self.data_list_for_search = dict()
        for table_key in self.excel_file:
            pd_table = self.excel_file[table_key]
            key_list = pd_table.keys()
            for key in key_list:
                if type(key) != str:
                    continue
                else:
                    self.data_list_for_search[key] = 0
                    for line_index in range(pd_table.shape[0]):
                        cell = pd_table.loc[line_index, key]
                        if type(cell) != str:
                            continue
                        else:
                            self.data_list_for_search[cell] = 0

    def __initiate_belongings_for_search__(self):
        self.data_belongings_for_search = dict()
        for table_key in self.excel_file:
            pd_table = self.excel_file[table_key]
            key_list = pd_table.keys()
            for key in key_list:
                if type(key) != str:
                    continue
                else:
                    for line_index in range(pd_table.shape[0]):
                        cell = pd_table.loc[line_index, key]
                        if type(cell) != str:
                            continue
                        else:
                            self.data_belongings_for_search[cell] = key

    def get(self, sheetname='', language=''):
        if sheetname == '' and language == '':
            raise ValueError('ExcelObject.get: parameter sheetname and language can be empty at the same time')
        elif sheetname != '':
            if sheetname not in self.sheetname2language_dict:
                raise IndexError('ExcelObject.get: parameter sheetname {0} not in Excel table'.format(sheetname))
            else:
                return self.excel_file[self.sheetname2language_dict[sheetname]]
        else:
            if language not in self.language2sheetname_dict:
                raise IndexError('ExcelObject.get: parameter language {0} not in Excel table'.format(language))
            else:
                return self.excel_file[language]

    def contain(self, element: str):
        return element in self.data_list_for_search

    def find_belongings(self, element: str):
        if element in self.data_belongings_for_search:
            return self.data_belongings_for_search[element]
        elif element not in self.data_belongings_for_search and element in self.data_list_for_search:
            return element
        else:
            return None

    def tags(self):
        return self.data_list_for_search.keys()

    def add(self, column: str, element: str):
        language = UnicodeStringRecognition().check_ustring_type(column)
        if language not in self.excel_file:
            raise IndexError('ExcelObject.add: colume {0} not in table'.format(column))
        else:
            if element in self.data_list_for_search:
                pass
            else:
                table = self.excel_file[language]
                flag = False
                for line_index in range(table.shape[0]):
                    if type(table.loc[line_index, column]) != str:
                        self.excel_file[language].loc[line_index, column] = element
                        flag = True
                    else:
                        continue
                if flag is False:
                    self.excel_file[language].loc[table.shape[0], column] = element
                self.__initiate_list_for_search__()

    def save(self, save_as=str()):
        if save_as != str():
            file_path = save_as
        else:
            file_path = self.excel_file_path
        writer = pd.ExcelWriter(path=file_path, engine='openpyxl')
        for table_key in self.excel_file:
            table = self.excel_file[table_key]
            table.to_excel(excel_writer=writer, sheet_name=self.language2sheetname_dict[table_key], na_rep='',
                           float_format=None, columns=None, header=True, index=False, index_label=None, startrow=0,
                           startcol=0, merge_cells=False, encoding=None, inf_rep='inf', verbose=False,
                           freeze_panes=None)
        writer.save()
        writer.close()


class BlackWhiteObject(ExcelObject):
    """
    ExcelTable defined to match the white/black lists
    sheetname - language map:
        chinese: 中文
    """
    def __initiate_words_transformation_dict__(self):
        self.sheetname2language_dict['中文'] = 'chinese'  # initiate sheetname - language transformation
        for key in self.sheetname2language_dict:
            self.language2sheetname_dict[self.sheetname2language_dict[key]] = key


class ToponymTable(ExcelObject):
    """
    ToponymTable defined to match the toponym
    sheetname - language map:
        chinese: 中文
    """
    def __initiate_list_for_search__(self):
        pass

    def __initiate_words_transformation_dict__(self):
        self.sheetname2language_dict['中国行政区'] = 'chinese'  # initiate sheetname - language transformation
        for key in self.sheetname2language_dict:
            self.language2sheetname_dict[self.sheetname2language_dict[key]] = key


if __name__ == '__main__':
    import time
    start_time = time.time()
    # ------------------------------
    # data = load_excel(path='../data/PackageDefinedPartitionExpression.xlsx')
    # print(data.keys(), type(data.keys()), data.shape[0], sep='\t')
    # print(data.loc[0, '分店'], type(data.loc[0, '分店']))
    # print(data.loc[0, '分行'], type(data.loc[0, '分行']))
    # print(type(data))
    # data = ExcelTable(excel_path='../data/PackageDefinedPartitionExpression.xlsx')
    data = ExcelObject(excel_path='../test.xlsx')
    data.add(column='分店', element='test01')
    data.add(column='分行', element='test02')
    print(data.excel_file['chinese'])
    data.save(save_as='../test.xlsx')
    # ------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration) // 3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: {0:d} h {1:d} m {2:.2f} s'.format(hour, minutes, seconds))
