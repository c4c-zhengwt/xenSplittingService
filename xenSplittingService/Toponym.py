# -*- encoding: UTF-8 -*-
# In this document a Toponym object is set up for checking land names
# All names should be encoded with utf-8

import os
import re
from xenSplittingService.ServiceComponents import load_excel, ExcelTable
######################################
# 把每个国家的地名组织成 ToponymStructure 定义的树状结构，
# 之后的的扩展只需要用 Toponym + countryname 的类定义新加入国家的
# 树状结构
# 新的地名搜索可以完成从小地名开始到其所属地名的链式搜索
######################################


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

admin_empty = ToponymAdministrationLevel(-2, 'None')
# ------------------------------------


# ------------------------------------
class ToponymStructure(object):
    def __init__(self, name: str, admin_level: ToponymAdministrationLevel, zip_code=str(), super_toponym=None):
        if len(name) == 0:
            raise ValueError('Toponym name could not be empty')
        self.name = str(name)
        self.place_code = zip_code
        self.administration_level = admin_level
        self.super_toponym = super_toponym
        self.sub_toponym = list()
        # self.name_translated = list() TODO: to solve location name translated to other languages

    def __repr__(self):
        sub_toponym_string = str()
        for toponym in self.sub_toponym:
            sub_toponym_string += ' ' + toponym.name
        if len(sub_toponym_string) > 0:
            sub_toponym_string += '  subtopolength:' + str(len(self.sub_toponym))
        else:
            sub_toponym_string += 'None'
        if self.super_toponym is None:
            super_toponym_string = 'None'
        else:
            super_toponym_string = self.super_toponym.name
        return '    '.join([
            'ToponymStructure name:', self.name,
            'place_code:', self.place_code,
            'admin_level:', self.administration_level.tag,
            'super_toponym:', super_toponym_string,
            'sub_toponym:', sub_toponym_string
        ])

    def add_subtoponym(self, sub_toponym_structure):
        if type(sub_toponym_structure) != ToponymStructure:
            raise TypeError('Method add_subtoponym of Class ToponymStructure received wrong input')
        else:
            sub_toponym_structure.super_toponym = self
            self.sub_toponym.append(sub_toponym_structure)

    def is_this_place(self, name: str):
        if name == self.name:
            return True
        elif self.name in name and self.administration_level.tag in name:
            return True
        elif name in self.name and (len(self.name)-len(name)) <= 1 and len(name) >= 2:
            return True
        else:
            return False
# ------------------------------------


# ------------------------------------
class Toponym(object):
    def __init__(self, data_path=os.path.join('data')):
        source_path = str(os.path.abspath(__file__))
        source_path = source_path.split(os.path.sep)
        while source_path[-1] != 'xenSplittingService':
            source_path.pop()
        while 'xenSplittingService' in source_path:
            source_path.remove('xenSplittingService')
        self.source_path = os.path.sep.join(source_path)
        self.data_path = data_path
        self.govern_level = dict()
        self.__objectification_govern_level__()
        self.__startup__()

    def check_location_name(self, name: str):
        # TODO: To check location in a better manner
        flag, tag = self.search_location_name(name)
        return flag

    def search_location_name(self, name: str):
        # TODO: To search name in different country
        return self.__recursively_search_name__(node=self.locations.sub_toponym[0], name=name)

    def __recursively_search_name__(self, node: ToponymStructure, name: str):
        flag = node.is_this_place(name)
        if flag:
            tag = node.name
            return flag, tag
        else:
            for item in node.sub_toponym:
                flag, tag = self.__recursively_search_name__(node=item, name=name)
                if flag:
                    return flag, node.name + ' ' + tag
            return False, ''

    def __startup__(self):
        self.locations = ToponymStructure(name='Earth', admin_level=self.govern_level['self'])
        chinese_toponym = ToponymChina(data_path=self.data_path)
        self.locations.add_subtoponym(chinese_toponym.location)

    def __objectification_govern_level__(self):
        """This method sets up the govern level for locations in a particular country"""
        self.govern_level['self'] = ToponymAdministrationLevel(level=-1, tag='Earth')

    def __identify_govern_level__(self, string_name):
        for key in self.govern_level:
            if key in string_name:
                return key
        return None


class ToponymChina(Toponym):
    def __startup__(self):
        table_pd = load_excel(os.path.join(self.source_path, self.data_path, 'ToponymInfomation.xlsx'),
                              sheetname='中国行政区')
        # table_pd = pd.read_excel(os.path.join(self.source_path, self.data_path, 'ToponymInfomation.xlsx'))
        self.location = ToponymStructure(name='中国', admin_level=self.govern_level['self'])
        node_basic = self.location
        node_one = node_two = node_three = node_basic
        __last_govern_level_list__ = [0, 0, 0, 0]
        for index_line in range(table_pd.shape[0]):
            __zip_code__ = str(table_pd.loc[index_line, '行政区划代码'])
            __govern_level_list__ = [int(__zip_code__[0:2]), int(__zip_code__[2:3]),
                                     int(__zip_code__[3:4]), int(__zip_code__[4:6])]
            __place_name__ = str(table_pd.loc[index_line, '名称'])
            __level_tag__ = self.__identify_govern_level__(__place_name__)
            if __level_tag__ is not None:
                __place_name__ = re.sub(__level_tag__, '', __place_name__)
                if len(__place_name__) == 0:
                    continue
                new_node = ToponymStructure(name=__place_name__, admin_level=self.govern_level[__level_tag__])
            else:
                new_node = ToponymStructure(name=__place_name__, admin_level=admin_empty)
            new_node.place_code = __zip_code__
            if __govern_level_list__[0] > __last_govern_level_list__[0]:
                node_basic.add_subtoponym(new_node)
                node_three = node_two = node_one = new_node
            elif __govern_level_list__[1] > __last_govern_level_list__[1] and __govern_level_list__[2] == 0:
                node_one.add_subtoponym(new_node)
                node_three = node_two = new_node
            elif __govern_level_list__[2] > __last_govern_level_list__[2] and __govern_level_list__[3] == 0 \
                    and __place_name__ != '辖区':
                node_two.add_subtoponym(new_node)
                node_three = new_node
            elif __place_name__ == '辖区':
                pass
            else:
                node_three.add_subtoponym(new_node)
            __last_govern_level_list__ = __govern_level_list__

    def __objectification_govern_level__(self):
        self.govern_level['self'] = ToponymAdministrationLevel(level=0, tag='中华人民共和国')
        self.govern_level['特别行政区'] = ToponymAdministrationLevel(1, '特别行政区')
        self.govern_level['自治区'] = ToponymAdministrationLevel(1, '自治区')
        self.govern_level['省'] = ToponymAdministrationLevel(1, '省')
        self.govern_level['市'] = ToponymAdministrationLevel(2, '市')
        self.govern_level['区'] = ToponymAdministrationLevel(3, '区')
        self.govern_level['县'] = ToponymAdministrationLevel(3, '县')
        self.govern_level['旗'] = ToponymAdministrationLevel(3, '旗')
        self.govern_level['自治州'] = ToponymAdministrationLevel(1, '自治州')
        self.govern_level['岛'] = ToponymAdministrationLevel(3, '岛')


if __name__ == '__main__':
    import time
    start_time = time.time()
    # -----------------------------------
    test_loc = Toponym(data_path=os.path.join('xenSplittingService', 'data'))
    print(test_loc.locations.sub_toponym[0].sub_toponym[8].sub_toponym[12])
    print(test_loc.search_location_name('浦东'))
    # print(test_loc.table, type(test_loc.table))
    # print(test_loc.check_location_name('兴安盟'))
    # -----------------------------------
    end_time = time.time()
    duration = end_time - start_time
    hour = int(duration) // 3600
    minutes = int(duration) // 60 - 60 * hour
    seconds = duration % 60
    print('\nRunning time: {0:d} h {1:d} m {2:.2f} s'.format(hour, minutes, seconds))
