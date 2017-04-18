# -*- encoding: UTF-8 -*-
# In this document a landname object is set up and names in china can be manipulated
import csv


class landname(object):
    def __init__(self):
        self.table = []
        self.province = []
        self.city = []
        self.district = []
        self.town = []
        self.selfgov = []
        self.flag = []
        self.island = []
        self.etcloc = []
        self.startup()

    def load_landname(self):  # read and write csv file
        """
        load a list which is of two dimension
        with lines in list and columns in sub_lists
        """
        try:
            csvfile = open('xingzhengqu.csv', 'r', newline='')
            spamreader = csv.reader(csvfile,
                                    delimiter=',',
                                    quotechar='|'
                                    )
            return [var for var in spamreader]
        except:
            return 0

    def update_landname(self):
        """
        save a list which is of two dimension to the file
        with lines in list and columns in sub_lists
        """
        try:
            csvfile = open('source_file/xingzhengqu.csv', 'w', newline='')
            spamwriter = csv.writer(csvfile,
                                    delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL
                                    )
            spamwriter.writerows()
            csvfile.close()
            return 1
        except:
            return 0

    def startup(self):
        self.table = self.load_landname()[1:]
        for line in self.table:
            if line[1][-1:] == '区':
                self.district.append([line[1][0:len(line[1])-1], '区', line[0][0:3], line[0][3:6]])
            elif line[1][-1:] == '县':
                if line[1] != '县':
                    self.town.append([line[1][0:len(line[1])-1], '县', line[0][0:3], line[0][3:6]])
            elif line[1][-1:] == '省':
                self.province.append([line[1][0:len(line[1])-1], '省', line[0][0:3], line[0][3:6]])
            elif line[1][-1:] == '市':
                self.city.append([line[1][0:len(line[1])-1], '市', line[0][0:3], line[0][3:6]])
            elif len(line[1]) >= 3:
                if line[1][-3:] == '自治州':
                    self.selfgov.append([line[1][0:len(line[1])-3], '自治州', line[0][0:3], line[0][3:6]])
                elif line[1][-1:] == '旗':
                    self.flag.append([line[1][0:len(line[1]) - 1], '旗', line[0][0:3], line[0][3:6]])
                elif line[1][-1:] == '岛':
                    self.island.append([line[1][0:len(line[1]) - 1], '岛', line[0][0:3], line[0][3:6]])
                else:
                    self.etcloc.append([line[1], '', line[0][0:3], line[0][3:6]])
            else:
                self.etcloc.append([line[1], '', line[0][0:3], line[0][3:6]])

    def checkLandname(self, name):
        if len(name) >= 3:
            if name[-1:] == '市':
                for location in self.city:
                    if location[0] == name[0:len(name) - 1]:
                        return name
            elif name[-1:] == '省':
                for location in self.province:
                    if location[0] == name[0:len(name) - 1]:
                        return name
            elif name[-1:] == '区':
                for location in self.district:
                    if location[0] == name[0:len(name) - 1]:
                        return name
            elif name[-1:] == '县':
                for location in self.town:
                    if location[0] == name[0:len(name) - 1]:
                        return name
            elif name[-3:] == '自治州':
                for location in self.town:
                    if location[0] == name[0:len(name) - 3]:
                        return name
            elif name[-1:] == '旗':
                for location in self.flag:
                    if location[0] == name[0:len(name) - 1]:
                        return name
            elif name[-1:] == '岛':
                for location in self.island:
                    if location[0] == name[0:len(name) - 1]:
                        return name
            else:
                for location in self.province:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.city:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.town:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.district:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.selfgov:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.flag:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.island:
                    if location[0] == name:
                        return (location[0]+location[1])
                for location in self.etcloc:
                    if location[0] == name:
                        return (location[0]+location[1])
        else:
            for location in self.province:
                if location[0] == name:
                    return (location[0]+location[1])
            for location in self.city:
                if location[0] == name:
                    return (location[0]+location[1])
            # for location in self.town:
            #     if location[0] == name:
            #         return (location[0]+location[1])
            # for location in self.district:
            #     if location[0] == name:
            #         return (location[0]+location[1])
            for location in self.selfgov:
                if location[0] == name:
                    return (location[0]+location[1])
            for location in self.flag:
                if location[0] == name:
                    return (location[0]+location[1])
            for location in self.island:
                if location[0] == name:
                    return (location[0]+location[1])
            for location in self.etcloc:
                if location[0] == name:
                    return (location[0]+location[1])
            return None


if __name__ == '__main__':
    import time
    start_time = time.time()
    #------------------------------------
    test_loc = landname()
    print(test_loc.table)
    print(test_loc.city)
    print(test_loc.province)
    print(test_loc.district)
    print(test_loc.town)
    print(test_loc.selfgov)
    print(test_loc.flag)
    print(test_loc.island)
    print(test_loc.etcloc)
    print(test_loc.checkLandname('通州'))
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration)//3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: %d h %d m %f s' % (hour, minutes, seconds))
