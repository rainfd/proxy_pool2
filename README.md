proxy_pool2

> 代理池

![效果截图](https://github.com/rainfd/proxy_pool2/blob/master/screenshoot/index.png)


## 功能说明

- 代理池中的代理是通过爬取网上免费代理获得
- 支持添加自定义代理爬虫
- 可通过api获取json代理列表: /api/proxy

| 参数        | 是否必填 | 参数说明    | 取值说明       |
| --------- | ---- | ------- | ---------- |
| page      | 否    | 当前页数    | 默认为20      |
| page_size | 否    | 每页条数    |            |
| https     | 否    | 支持HTTPS | ture/false |
| anonymous | 否    | 匿名      | true/false |

json格式

```json
{
  "proxies": [{
    "ip": "12.12.12.12",
    "port": 80,
    "https": true,
    "anonymous": false,
    "delay": 3.0,
    "location": "北京",
    "validate_time": "2017/01/01 00:00"
  }],
  "total": 100
}
```



## 使用技术

Python3.5+

### 前端

- Vue
- Element-ui
- vue-resource

### 后端

- Flask
- Apscheduler
- Pymongo
- Gunicorn

## 安装&启动

安装数据库和Python依赖

```shell
> sudo apt-get install mongodb
> git clone https://github.com/rainfd/proxy_pool2
> cd proxy_pool2
> pip install -r requirements.txt
```

启动爬虫

```
> python3 manager.py crawl
```

启动服务

```
> gunicorn app:app --bind:0.0.0.0:8000 -w 5
```

等待爬虫进行一段时间后，访问[http://localhost:8000](http://localhost:8000)即可看到代理列表。

### 添加自定义代理爬虫

 在proxygetter/spider下创建新的文件myspider.py

```python
from proxygetter.proxyspider import ProxySpider

class MYSpider(ProxySpider):
    def get_proxy(self):
        """代理格式:
        proxy = {
          'ip': '12.12.12.12',
          'port': 80,
          'location': ‘北京',
          'https': True,
          'anonymous': False
        }
        """
        yield proxy
```

然后在settings.py中添加爬虫名称和请求间隔

```python
SPIDER_MODULES = {
    # ...
    'myspider.MYSPIDER': 0,
}
```

