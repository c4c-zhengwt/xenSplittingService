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

# --------------------------------------------------------
class MultiList(object):
    def __init__(self, components: list):
        self.lists = dict()
        for tag in components:
            if type(tag) != str:
                raise ValueError('MultiList.__init__(components): expected str in parameter components')
            self.lists[tag] = list()

    def contain(self, element):
        flag = False
        for tag in self.lists:
            if element in self.lists[tag]:
                flag = True
        return flag

    def tags(self):
        return self.lists.keys()

    def append(self, tag: str, element):
        try:
            self.lists[tag].append(element)
        except KeyError:
            raise KeyError('MultiList.append(tag, x): tag not in MultiList')

    def remove(self, tag: str, element):
        try:
            self.lists[tag].remove(element)
        except KeyError:
            raise KeyError('MultiList.remove(tag, x): tag not in MultiList')
        except ValueError:
            raise ValueError('MultiList.remove(tag, x): x not in MultiList')
# --------------------------------------------------------


# --------------------------------------------------------
if __name__ == '__main__':
    pass
