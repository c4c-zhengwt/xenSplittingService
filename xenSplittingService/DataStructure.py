# -*- encoding: UTF-8 -*-
# --------------------------------------------------------
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
class CountingDict(object):
    def __init__(self):
        self.stored_dict = dict()

    def count(self, element):
        if element in self.stored_dict:
            self.stored_dict[element] += 1
        else:
            self.stored_dict[element] = 1

    def get(self, tag: str):
        if tag not in self.stored_dict:
            raise IndexError('CountingDict.get tag {0} not in dict'.format(tag))
        else:
            return self.stored_dict[tag]

    def set(self, tag: str, element):
        self.stored_dict[tag] = element

    def keys(self):
        return self.stored_dict.keys()

    def results(self):
        return self.stored_dict

    def sort_by_weights(self, inverse=False):
        stored_list = list(self.stored_dict)
        for index_x in range(len(stored_list)):
            for index_y in range(index_x + 1, len(stored_list)):
                if self.stored_dict[stored_list[index_x]] > self.stored_dict[stored_list[index_y]]:
                    stored_list[index_x], stored_list[index_y] = stored_list[index_y], stored_list[index_x]
        if inverse is True:
            inverse_list = list()
            for index in range(len(stored_list)):
                inverse_list.append(stored_list[index])
            return inverse_list
        else:
            return stored_list
# --------------------------------------------------------


# --------------------------------------------------------
if __name__ == '__main__':
    import time
    start_time = time.time()
    # ------------------------------
    # ------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration) // 3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: {0:d} h {1:d} m {2:.2f} s'.format(hour, minutes, seconds))
