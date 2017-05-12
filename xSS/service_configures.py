# -*- encoding: UTF-8 -*-
# --------------------------------------------------------
import csv
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


def append_table_to_csv_2d(filename, content):
    csvfile = open(filename, 'a', encoding='utf-8', newline='\n')
    spamwriter = csv.writer(csvfile,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL
                            )
    spamwriter.writerows(content)
    csvfile.close()


def save_csv_2d(filename, content):
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

if __name__ == '__main__':
    pass
