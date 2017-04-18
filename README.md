# xenSplittingService

The splitting service splitting company names and bill memos is
designed for Xencio

现有功能：
- splitting：单纯切词，返回以空格分割的单词串
- splitfirmname：对公司名称进行更准确的切词，返回以空格分割的单词串，单词按
位置具有意义如下
    - 第一位置：公司地域，若为空则为 "-"


待实现功能：
- 获取公司经营范围白名单之后增强splitfirmname



---

## 部署要求

所有python代码均基于python 3.4且测试通过

本切词服务需要配置以下包：

- re，正则表达式包（已包含在python3.4中）
- csv，逗号分隔值文件（已包含在python3.4中）
- jieba，结巴分词包（分词包来源：https://github.com/fxsjy ）

---

本切词服务共包含以下文件：

- SplittingService.md
- SplittingService.py
- china_landname.py
- splittingdict.txt
- xingzhengqu.csv

其中 SplittingService.py 为主服务文件；china_landname.py 为判断一个字符串是否是中国行政地名的文件；splittingdict.txt 为分词字典所需要的自定义参考字典；xingzhengqu.csv是中国行政区清单

---

## 调用方式

运行SplittingService.py，获取本地IP和端口如 http://127.0.0.1:8080

使用GET方法调用，例如：
```python
import requests
s = requests.session()
r = s.get('http://127.0.0.1:8080/splitting', params = {'content': '无锡市外服人力资源有限公司'})
r.status_code, r.text
r = s.get('http://127.0.0.1:8080/splitfirmname', params = {'content': '无锡市外服人力资源有限公司'})
r.status_code, r.text
```

返回：

    >>> '无锡市 外服 人力资源 有限公司'
    >>> '无锡市 外服 人力资源 有限公司'



