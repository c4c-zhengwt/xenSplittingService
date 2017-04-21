# xenSplittingService

## 开始使用

本服务基于python 3，请确保已安装setuptools包

Terminal安装

    git clone --recursive https://github.com/mingotang/xenSplittingService
    cd xenSplittingService

若运行环境仅使用Python 3：

    python setup.py install

若运行环境同时使用Python 2&3

    python3 setup.py install

## 调用方式

创建服务对象以初始化自定义字典信息、名称白名单、名称黑名单和服务类型白名单

    import xenSplittingService as xSS
    splitter = xSS.ContentSplit()

#### 单纯切词：

返回以空格分割的单词串

    splitter.split('无锡市外服人力资源有限公司')
    >>> 无锡市 外服 人力资源 有限公司

#### 对公司名称进行更准确的切词：

    splitter.split_firmname('无锡市外服人力资源有限公司')
    >>> 无锡市 有限公司 外服 人力资源

返回以空格分割的单词串，单词按位置具有意义如下

- 第一位置：公司地域，若为空则为 "-"
- 第二位置：公司类型，若为空则为 "-"

> 注：公司类型由 `data/Company Type Whitelist.csv`定义


待实现功能：
- 获取公司经营范围白名单之后增强splitfirmname


## 修改配置文件


本切词服务共包含以下配置文件：


splittingdict.txt 为分词字典所需要的自定义参考字典；

xingzhengqu.csv是中国行政区清单



