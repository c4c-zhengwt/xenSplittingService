# -*- encoding: UTF-8 -*-
# In this document a Toponym object is set up for checking land names
# All names should be encoded with utf-8

import os
import pandas as pd


# ------------------------------------
class ToponymAdministrationLevel(object):
    """
    Represent the administration level of a paticular place,
    The Earth starts with level -1
    Any country starts with level 0
    """
    def __init__(self, level: int, tag: str):
        self.level = level
        self.tag = tag
        # self.tag_translated = list()
    # ToDO: rewrite __repr__


admin_level_earth = ToponymAdministrationLevel(level=-1, tag='Earth')
# ------------------------------------


# ------------------------------------
class ToponymStructure(object):
    def __init__(self, name: str, admin_level: ToponymAdministrationLevel, zip_code=str(), super_toponym=None):
        self.name = str(name)
        self.zip_code = zip_code
        self.administration_level = admin_level
        self.super_toponym = super_toponym
        self.lower_toponym = list()
        # self.name_translated = list() TODO: to solve location name translated to other languages
    # ToDO: rewrite __repr__

    def add_subtoponym(self, sub_toponym):
        if type(sub_toponym) != ToponymStructure:
            raise ValueError()
        self.lower_toponym.append(sub_toponym)
        sub_toponym.super_toponym = self

    def is_this_place(self, name: str):
        if name == self.name:
            return True
        else:
            return False
# ------------------------------------


# ------------------------------------
class Toponym(object):
    def __init__(self):
        source_path = str(os.path.abspath(__file__))
        source_path = source_path.split(os.path.sep)
        while source_path[-1] != 'xenSplittingService':
            source_path.pop()
        while 'xenSplittingService' in source_path:
            source_path.remove('xenSplittingService')
        self.source_path = os.path.sep.join(source_path)
        self.__startup__()

    def check_location_name(self, name: str):
        raise NameError('The location name checking process for for Basic LandName class is not defined.')

    def __startup__(self):
        self.locations = ToponymStructure(name='Earth', admin_level=admin_level_earth)
        chinese_landname = ToponymChina()

    def __objectification_chinese_toponym__(self):
        table_pd = pd.read_excel(os.path.join(self.source_path, 'xenSplittingService', 'data', 'ToponymChinese.xlsx'))
        table_pd = pd.DataFrame()
        for index_line in range(table_pd.shape[0]):


class ToponymChina(Toponym):
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

    def check_location_name(self, name):
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
    test_loc = ToponymChina()
    # print(test_loc.table, type(test_loc.table))
    print(test_loc.city)
    print(test_loc.province)
    print(test_loc.district)
    print(test_loc.town)
    print(test_loc.selfgov)
    print(test_loc.flag)
    print(test_loc.island)
    print(test_loc.etcloc)
    print(test_loc.check_location_name('兴安盟'))
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration)//3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: %d h %d m %f s' % (hour, minutes, seconds))
