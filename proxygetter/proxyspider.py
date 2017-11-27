import random
import time
import logging

import requests
from lxml import etree

from proxygetter.logger import logger
from proxygetter.utils import from_object


class DataClass(type):

    @property
    def validate_data(cls):
        cls._validate_data = {}
        from_object(cls._validate_data, 'proxygetter.validate_data')
        return cls._validate_data


class ProxySpider(metaclass=DataClass):
    _validate_data = {}

    def __init__(self, interval=0):
        self.interval = interval

    def get_proxy(self):
        """Yield a proxy dictionary
        Example:
        {
            'ip': 12.12.12.12, type: str
            'port': 8000, type: int
            'https': False, type: bool
            'anonymous': True, type: bool
            'location': '北京', type: bool
            'delay': 3, type: float
            # 'validate_time': '2017-01-01-01:01:01' set by program automatically
        }
        """

    def parse(self, url, headers=None, proxies=None):
        time.sleep(self.interval)
        return self.html_tree(url, headers, proxies)

    @staticmethod
    def html_tree(url, headers=None, proxies=None):
        """Use lxml to construct the html tree.
        Next parse it by xpath(e.g. tree.xpath('')).
        """
        # time.sleep(cls._interval)
        response = requests.get(url, headers, proxies=proxies)
        if response.status_code != 200:
            return None
        tree = etree.HTML(response.text)
        return tree

    @classmethod
    def validate(cls, proxy):
        """proxy: {
            'ip': '12.12.12.12',
            'port': 900,
            'https': True
        }
        """
        try:
            if proxy['https']:
                url = random.choice(cls.validate_data['HTTPS_URL'])
                proxies = {'https': 'https://' + proxy['ip'] + ':' + str(proxy['port'])}
            else:
                url = random.choice(cls.validate_data['HTTP_URL'])
                proxies = {'http': 'http://' + proxy['ip'] + ':' + str(proxy['port'])}
            t = time.time()
            response = requests.get(url, proxies=proxies)
            delay = round((time.time() - t) / 2, 2)
            if response.status_code == 200:
                return delay
        except Exception as e:
            logger.warning(e)
            return False


if __name__ == '__main__':
    url = 'http://www.x.com'
    proxies = {
        'http': 'http://111.200.58.94:80'
    }
    r = requests.get(url, proxies=proxies)
    print(r.status_code)
    proxy = {
        'ip': '211.72.193.130',
        'port': 8080,
        'https': False
    }
    x = ProxySpider.validate(proxy)
    if x:
        print('pass 2')
