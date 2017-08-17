# -*- encoding: UTF-8 -*-
# --------------------------------------------------------
import csv
import pandas as pd
from xenSplittingService.WordRecognition import UnicodeStringRecognition
# --------------------------------------------------------


# --------------------------------------------------------
# read and write csv file
def load_csv(filename):
    """
    load a list which is of two dimension
    with lines in list and columns in sub_lists
    """
    csvfile = open(filename, 'r', encoding='utf-8', newline='')
    spamreader = csv.reader(csvfile,
                            delimiter=',',
                            quotechar='"'
                            )
    return [var for var in spamreader]


def save_csv(filename, content):
    """
    save a list which is of two dimension to the file
    with lines in list and columns in sub_lists
    """
    csvfile = open(filename, 'w', encoding='utf-8', newline='')
    spamwriter = csv.writer(csvfile,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL
                            )
    spamwriter.writerows(content)
    csvfile.close()
    return True
# --------------------------------------------------------


# --------------------------------------------------------
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
# --------------------------------------------------------


# --------------------------------------------------------
class ExcelTable(object):
    def __init__(self, excel_path: str,
                 header=0, skiprows=None, skip_footer=0, index_col=None, names=None,
                 parse_cols=None, parse_dates=False, date_parser=None, na_values=None, thousands=None,
                 convert_float=True, has_index_names=None, converters=None, dtype=None, true_values=None,
                 false_values=None, engine=None, squeeze=False
                 ):
        self.excel_file_path = excel_path
        excel_file_chi = pd.read_excel(excel_path, sheetname='中文', header=header, skiprows=skiprows,
                                       skip_footer=skip_footer, index_col=index_col, names=names,
                                       parse_cols=parse_cols, parse_dates=parse_dates, date_parser=date_parser,
                                       na_values=na_values, thousands=thousands, convert_float=convert_float,
                                       has_index_names=has_index_names, converters=converters, dtype=dtype,
                                       true_values=true_values, false_values=false_values, engine=engine,
                                       squeeze=squeeze)
        self.excel_file = dict()
        self.excel_file['chinese'] = excel_file_chi
        self.data_list_for_search = dict()
        self.__initiate_list_for_search__()

    def __initiate_list_for_search__(self):
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

    def contain(self, element: str):
        return element in self.data_list_for_search

    def add(self, colume: str, element: str):
        language = UnicodeStringRecognition().check_ustring_type(colume)
        if language not in self.excel_file:
            raise IndexError('ExcelTable.add: colume {0} not in table'.format(colume))
        else:
            if element in self.data_list_for_search:
                pass
            else:
                table = self.excel_file[language]
                flag = False
                for line_index in range(table.shape[0]):
                    if type(table.loc[line_index, colume]) != str:
                        self.excel_file[language].loc[line_index, colume] = element
                        flag = True
                    else:
                        continue
                if flag is False:
                    self.excel_file[language].loc[table.shape[0], colume] = element
# --------------------------------------------------------


# --------------------------------------------------------
if __name__ == '__main__':
    import time
    start_time = time.time()
    # ------------------------------
    # data = load_excel(path='../data/PackageDefinedPartitionExpression.xlsx')
    # print(data.keys(), type(data.keys()), data.shape[0], sep='\t')
    # print(data.loc[0, '分店'], type(data.loc[0, '分店']))
    # print(data.loc[0, '分行'], type(data.loc[0, '分行']))
    # print(type(data))
    data = ExcelTable(excel_path='../data/PackageDefinedPartitionExpression.xlsx')
    data.add(colume='分店', element='test')
    data.add(colume='分行', element='test')
    print(data.excel_file['chinese'])
    # ------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration) // 3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: {0:d} h {1:d} m {2:.2f} s'.format(hour, minutes, seconds))
