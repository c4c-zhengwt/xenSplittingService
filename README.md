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

    splitter.split_firmname('无锡市外服人力资源有限公司', enable_english_output=True)
    >>> 无锡市 有限公司 外服 人力资源

返回以空格分割的单词串，单词按位置具有意义如下

- 第一位置：公司地域，如北京市，若为空则为 "-"
- 第二位置：公司类型，如有限公司，若为空则为 "-" （配置文件待补充）
- 第三位置：公司经营类型，如超市，若为空则为 "-" （配置文件待补充）

参数中 `enable_english_output=True` 为是否允许英文字母在中文名字的结果中输出，默认为False

> 注：公司类型由 `data/package_com_type_whitelist.csv`定义
> 用户自定义公司类型配置文件为 `data/User_defined_company_type_whitelist.csv`，用户可以使用类方法添加，添加方法见`修改配置文件`


## 修改配置文件


本切词服务共包含以下配置文件：

---

- 包内置配置文件：（该类配置文件在安装时会覆盖前一个版本的配置文件）
    - data/package_com_keyword_blacklist.csv 分词输出的黑名单，黑名单当中的内容将不会被输出
    - data/package_com_service_type_whitelist.csv 公司经营服务类型的白名单
    - data/package_com_type_whitelist.csv  公司类型的白名单
    - data/pre_usr_identified_dict 切词之前的配置文件
    - data/XingZhenQu.csv 中国行政区名字文件

### 内置配置文件修改方式：

    data/package_com_keyword_blacklist.csv

这三个文件为逗号分隔值文件，修改之时可以在文件末新建一行上面输入多个值并用（英文）逗号分开，也可以在文件末每行输入一个参数

    data/pre_usr_identified_dict

该文件为文本文件，修改之时需要遵守一定的输入参数规格：单词（空格）频率（空格）类型。如 `备付金 100 n` 其中n为单词的英文语法中类型，其他如动词（v）、地名（s）。事实上本文件在分词包开发之时已做过调整，不建议修改。

    data/XingZhenQu.csv

该文件为逗号分隔值文件，按行政区代码（英文逗号）名称的格式构建，不建议修改。

---

- 用户自定义配置文件：
    - data/User_defined_company_keyword_blacklist.csv 分词输出的黑名单，黑名单当中的内容将不会被输出
    - data/User_defined_company_service_type_whitelist.csv 公司经营服务类型的白名单
    - data/User_defined_company_type_whitelist.csv 公司类型的白名单

### 用户自定义配置文件修改方式：

直接修改：如内置配置文件

类方法修改：

    import xenSplittingService as xSS
    splitter = xSS.ContentSplit()
    splitter.add_company_type(param)
    splitter.add_company_service_type(param)
    splitter.add_blocked_company_keyword(param, force_add=True)

其中param可以是单个字符串如：`'人力资源'` ，也可以是字符串组成的列表如：`['人力资源', '外服']`。如果配置文件当中已经存在相关字段或者类似文件当中存在相关字段则不会加入用户自定义配置文件，若要强行加入请使用可选参数 `force_add=True`

> 类似配置文件指的是 company type 和 company service type 这两个文件相类似。



## 待实现功能：

- 英文公司名字和备注的分词


