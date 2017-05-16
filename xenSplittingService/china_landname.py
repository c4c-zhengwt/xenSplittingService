# -*- encoding: UTF-8 -*-
# In this document a landname object is set up and names in china can be manipulated
import os
from xenSplittingService.service_configures import *


class LandName(object):
    def __init__(self):
        source_path = os.path.abspath(__file__)
        source_path = source_path.split(os.path.sep)
        while source_path[-1] != 'xenSplittingService':
            source_path.pop()
        while 'xenSplittingService' in source_path:
            source_path.remove('xenSplittingService')
        # while source_path.count('xenSplittingService') >= 1:
        #     source_path.remove('xenSplittingService')
        self.source_path = os.path.sep.join(source_path)
        self.path_china_land_names_csv = os.path.join(self.source_path, 'data',
                                                      'XingZhenQu.csv')
        try:
            self.table = load_csv(self.path_china_land_names_csv)[1:]
        except FileNotFoundError:
            self.path_china_land_names_csv = os.path.join(self.source_path,
                                                          'xenSplittingService',
                                                          'data',
                                                          'XingZhenQu.csv')
            self.table = load_csv(self.path_china_land_names_csv)[1:]
        self.table = list()
        self.province = list()
        self.city = list()
        self.district = list()
        self.town = list()
        self.selfgov = list()
        self.flag = list()
        self.island = list()
        self.etcloc = list()
        self.__startup__()

    def __startup__(self):
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

    def check_landname(self, name):
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
                        return location[0]+location[1]
                for location in self.city:
                    if location[0] == name:
                        return location[0]+location[1]
                for location in self.town:
                    if location[0] == name:
                        return location[0]+location[1]
                for location in self.district:
                    if location[0] == name:
                        return location[0]+location[1]
                for location in self.selfgov:
                    if location[0] == name:
                        return location[0]+location[1]
                for location in self.flag:
                    if location[0] == name:
                        return location[0]+location[1]
                for location in self.island:
                    if location[0] == name:
                        return location[0]+location[1]
                for location in self.etcloc:
                    if location[0] == name:
                        return location[0]+location[1]
        else:
            for location in self.province:
                if location[0] == name:
                    return location[0]+location[1]
            for location in self.city:
                if location[0] == name:
                    return location[0]+location[1]
            # for location in self.town:
            #     if location[0] == name:
            #         return location[0]+location[1]
            # for location in self.district:
            #     if location[0] == name:
            #         return location[0]+location[1]
            for location in self.selfgov:
                if location[0] == name:
                    return location[0]+location[1]
            for location in self.flag:
                if location[0] == name:
                    return location[0]+location[1]
            for location in self.island:
                if location[0] == name:
                    return location[0]+location[1]
            for location in self.etcloc:
                if location[0] == name:
                    return location[0]+location[1]
            return None


if __name__ == '__main__':
    import time
    start_time = time.time()
    # -----------------------------------
    test_loc = LandName()
    print(test_loc.table)
    print(test_loc.city)
    print(test_loc.province)
    print(test_loc.district)
    print(test_loc.town)
    print(test_loc.selfgov)
    print(test_loc.flag)
    print(test_loc.island)
    print(test_loc.etcloc)
    print(test_loc.check_landname('兴安盟'))
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration)//3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: %d h %d m %f s' % (hour, minutes, seconds))
