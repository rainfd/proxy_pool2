from proxygetter.proxyspider import ProxySpider

"""Yield a proxy dictionary
Example:
{
    'ip': 12.12.12.12,
    'port': 8000,
    'protocol': 'HTTP',
    'anonymous': True,
    'location': '北京',
    'delay': 3,
    'validate': '2017-01-01-01:01:01'
}
"""


class KDLSpider(ProxySpider):
    # interval = 1

    def get_proxy(self):
        """http"""
        start_url = 'http://www.kuaidaili.com/free/inha/'
        pages = range(1, 2)
        urls = [start_url + str(x) for x in pages]
        for url in urls:
            tree = self.parse(url)
            for x in tree.xpath('//tbody/tr'):
                proxy = {
                    'ip': x.xpath('td[1]/text()')[0],
                    'port': int(x.xpath('td[2]/text()')[0]),
                    'anynoums': True,
                    'https': False,
                    'location': x.xpath('td[5]/text()')[0],
                }
                yield proxy
                # 502 error occur if fetch too fast
                # time.sleep(1)


if __name__ == '__main__':
    spider = KDLSpider()
    proxy = spider.get_proxy()
    print(proxy)
