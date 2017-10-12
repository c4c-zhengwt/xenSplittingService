# xenSplittingService

## 配置

本服务基于python 3，请确保已安装setuptools包

Terminal安装

    git clone --recursive https://github.com/mingotang/xenSplittingService
    cd xenSplittingService


若运行环境同时使用Python 2&3

    python3 setup.py install

## 调用

创建服务对象以初始化自定义字典信息、名称白名单、名称黑名单和服务类型白名单。


```python
import xenSplittingService as xSS
splitter = xSS.ContentSplit()

```


#### 单纯切词：

返回以空格分割的单词串
```Python
split('无锡市外服人力资源有限公司', **kwargs)
split('无锡市外服人力资源有限公司', unable_digit=True)
```

    >>> 无锡市 外服 人力资源 有限公司
    
`**kwargs`可选参数：
- unable_digit=True
- unable_english=True
- unable_chinese=True

> 参数 unable_*** 在 kwargs 当中出现就意味着禁止生效，其值为True或者False都不会改变这一点
> 这个分词不会过滤黑名单


#### 对公司名称进行更准确的切词：
```Python
split_firm_name('无锡市外服人力资源有限公司', **kwargs)
```

    >>> 无锡市 有限公司 外服 人力资源

返回以空格分割的单词串，单词按位置具有意义如下

- 第一位置：公司地域，如北京市，若为空则为 "-"
- 第二位置：公司类型，如有限公司，若为空则为 "-" （配置文件待补充）
- 第三位置：公司经营类型，如超市，若为空则为 "-" （配置文件待补充）

> kwargs 参数见上文

#### 对备注进行分词


```Python
split_msg('无锡市外服人力资源有限公司', **kwargs)
```

> kwargs 参数见上文
> 和一般分词的区别在于会过滤黑名单


## 修改配置文件

### 配置文件组织方式：

本切词服务共包含以下配置文件（现阶段因为需要手动复制data文件夹似乎内置配置文件和用户配置文件是同样的结果）：


---

- 包内置配置文件：
    - data/PackageDefinedKeywordBlacklist.xlsx 分词输出的黑名单，黑名单当中的内容将不会被输出
    - data/PackageDefinedServiceTypeWhitelist.xlsx 公司经营服务类型的白名单
    - data/PackageDefinedFirmTypeWhitelist.xlsx  公司类型的白名单
    - data/PackageDefinedPartitionExpression.xlsx 分公司、分部等表达方式文件
    - data/ToponymInfomation.xlsx 行政区名字文件
    - data/DeveloperDefinedAdjustment.txt 切词之前的配置文件

### 内置配置文件修改方式：

直接打开修改后保存即可



## API demo功能：

本包可以直接运行包内的 `web_cache.py` 进行API功能展示

请确保已安装以下扩展包：

- cherrypy
- requests
- jieba

### demo 例子

先在命令行中运行

    python3 web_cache.py


获得本机服务口例如`'http://127.0.0.1:8080/'`，可以使用以下方式进行demo：

```Python
import requests
s = requests.Session()
r = s.get('http://127.0.0.1:8080/', params={'words': '无锡市外服人力资源有限公司', 'method': '1', 'unable': 'digit|other'})
```

    {'content': ['无锡市', '有限公司', '人力资源', '外服']}


其中method参数设置如下：
- '0'：一般分词，不过滤黑名单，见上文中 `splitter.split()`
- '1'：公司名分词，会过滤黑名单，见上文中 `splitter.split_firmname()`
- '2'：备注分词，会过滤黑名单见上文中 `splitter.split_msg()`

unable参数设置如下：
- 用 `'|'` 隔开需要禁止的词类型
- 可禁止类型列表：'english', 'chinese', 'digit', 或参考文件 `xenSplittingService/ServiceComponents.py` 中的 UnicodeCharacterRecognition.language_base
