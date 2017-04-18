# -*- encoding: UTF-8 -*-
# In this document firm name and remarks are segmented
# --------------------------
import cherrypy
import jieba
import re
import china_landname
# --------------------------


# ------------------------------------


# ------------------------------------
class ContentSplit(object):
    def __init__(self):
        jieba.load_userdict("../data/pre_usr_identified_dict")

    def is_eng_name(self, name):
        name = re.sub(r'\W', "", name)
        count = 0
        for char in name:
            if self.__is_english_char(char) == 1:
                count += 1
        if count/len(name) >= 0.6:
            return 1
        else:
            return 0

    def is_chi_name(self, name):
        name = re.sub(r'\W', "", name)
        count = 0
        for char in name:
            if self.__is_chinese_char(char) == 1:
                count += 1
        if count/len(name) >= 0.6:
            return 1
        else:
            return 0

    def __is_english_char(self, uchar):
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False

    def __is_chinese_char(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    def split_firmname(self, name):
        if self.is_chi_name(name):
            return ' '.join(self.split_firmname_zh(name))
        else:
            return ''

    def split_firmname_zh(self, name):
        item_text = jieba.cut(str(name))
        namelist = list(item_text)
        while '\u3000' in namelist:
            namelist.remove('\u3000')
        location = china_landname.landname()
        nameline = []
        # ---------------------------------------------------------- derive location
        if '分公司' not in namelist:
            if location.checkLandname(namelist[0]) != None:
                nameline.append(location.checkLandname(namelist[0]))
                del namelist[0]
            else:
                if '中国' not in namelist:
                    if '(' in namelist and ')' in namelist:
                        aindex = namelist.index('(')
                        bindex = namelist.index(')')
                        if bindex - aindex > 1:
                            for index in range(aindex+1, bindex, 1):
                                if len(nameline) == 0:
                                    if location.checkLandname(namelist[index]) != None:
                                        nameline.append(location.checkLandname(namelist[index]))
                                        del namelist[index]
                    else:
                        if '(' in namelist:
                            aindex = namelist.index('(')
                            for index in range(aindex + 1, len(namelist), 1):
                                if len(nameline) == 0:
                                    if location.checkLandname(namelist[index]) != None:
                                        nameline.append(location.checkLandname(namelist[index]))
                                        del namelist[index]
                        else:
                            for index in range(1, len(namelist), 1):
                                if len(nameline) == 0:
                                    if location.checkLandname(namelist[index]) != None:
                                        nameline.append(location.checkLandname(namelist[index]))
                                        del namelist[index]
                            if len(nameline) == 0:
                                nameline.append('-')
                            pass    # no location
                    if len(nameline) == 0:
                        nameline.append('-')
                else:
                    namelist.remove('中国')
                    for index in range(len(namelist)):
                        if len(nameline) == 0:
                            if location.checkLandname(namelist[index]) != None:
                                nameline.append(location.checkLandname(namelist[index]))
                                del namelist[index]
                    if len(nameline) == 0:
                        nameline.append('-')
        else:
            tailindex = namelist.index('分公司')
            if tailindex >= 1:
                formerindex = 0
                for i in range(tailindex-1, -1, -1):
                    if '公司' in namelist[i]:
                        formerindex = i
                for j in range(formerindex+1, tailindex, 1):
                    if location.checkLandname(namelist[j]) != None:
                        nameline.append(location.checkLandname(namelist[j]))
                        del namelist[j]
                if len(nameline) == 0:
                    if location.checkLandname(namelist[0]) != None:
                        nameline.append(location.checkLandname(namelist[0]))
                        del namelist[0]
                    else:
                        for index in range(1, formerindex, 1):
                            if len(nameline) == 0:
                                if location.checkLandname(namelist[index]) != None:
                                    nameline.append(location.checkLandname(namelist[index]))
                                    del namelist[index]
                if len(nameline) == 0:
                    nameline.append('-')
            else:
                if len(nameline) == 0:
                    if location.checkLandname(namelist[0]) != None:
                        nameline.append(location.checkLandname(namelist[0]))
                        del namelist[0]
                if len(nameline) == 0:
                    nameline.append('-')
        # ---------------------------------------------------------- cleanning
        for i in range(len(namelist)):
            namelist[i] = re.sub(r'\W', "", namelist[i])
        while '' in namelist:
            namelist.remove('')
        # ---------------------------------------------------------- merging
        indexlist = []
        skiplist = []
        for item in namelist:
            if len(item) == 1:
                indexlist.append(namelist.index(item))
        for i in range(len(indexlist)):
            if i not in skiplist:
                content = namelist[indexlist[i]]
                for j in range(i+1, len(indexlist), 1):
                    if j == i + indexlist[j] - indexlist[i]:
                        content += namelist[indexlist[j]]
                        skiplist.append(j)
                namelist[indexlist[i]] = content
        skiplist.reverse()
        for item in skiplist:
            del namelist[indexlist[item]]
        if '有限公司' in namelist:
            pass
        # ---------------------------------------------------------- appending last items
        for item in namelist:
            nameline.append(item)
        return nameline

    def split_mome(self, content):
        item_text = jieba.cut(str(content))
        item_text = list(item_text)
        for i in range(len(item_text)):
            item_text[i] = re.sub(r'\W', "", item_text[i])
        while '' in item_text:
            item_text.remove('')
        return ' '.join(item_text)

    def split(self, content):
        item_text = jieba.cut(str(content))
        item_text = list(item_text)
        for i in range(len(item_text)):
            item_text[i] = re.sub(r'\W', "", item_text[i])
        while '' in item_text:
            item_text.remove('')
        return ' '.join(item_text)


# ------------------------------------
class SplittingService(object):
    def __init__(self):
        pass

@cherrypy.expose
class splitting(object):
    def __init__(self):
        self.splitter = ContentSplit()

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, content):
        return self.splitter.split(content)

@cherrypy.expose
class splitfirmname(object):
    def __init__(self):
        self.splitter = ContentSplit()

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, content):
        return self.splitter.split_firmname(content)

@cherrypy.expose
class splitremarks(object):
    def __init__(self):
        self.splitter = ContentSplit()

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, content):
        return self.splitter.split_mome(content)


if __name__ == '__main__':
    import random
    import string
    # ------------------------------------

    root = SplittingService()
    root.splitfirmname = splitfirmname()
    root.splitremarks = splitremarks()
    root.splitting = splitting()

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            }
        }
    cherrypy.quickstart(root, '/', conf)

    # -----------------------------------
    # -----------------------------------
