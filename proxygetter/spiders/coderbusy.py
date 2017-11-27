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


class CoderBusy(ProxySpider):

    def get_proxy(self):
        '''
        # anymous normal
        start_url = 'https://proxy.coderbusy.com/zh-cn/classical/anonymous-type/anonymous/p{}.aspx'
        urls = [start_url.format(i) for i in range(1, 4)]
        for url in urls:
            tree = self.html_tree(url)
            for x in tree.xpath('//tbody/tr'):
                proxy = {}
                proxy['ip'] = x.xpath('td[1]/span/text()')[0]
                port = x.xpath('td[2]/script/text()')[0]
                proxy['port'] = ''.join(x for x in port if x in '0123456789')
                location = x.xpath('td[3]/a/text() | td[3]/text()')
                proxy['location'] = ''.join([x.strip() for x in location])
                elm = x.xpath('td[8]/i')
                proxy['https'] = True if len(elm) else False
                proxy['delay'] = float(x.xpath('td[10]/text()')[0][:-1])
                proxy['anynoums'] = True
                yield proxy
        '''
        # non anynoums
        pages = 10
        non_url = 'https://proxy.coderbusy.com/zh-cn/classical/anonymous-type/transparent/p{}.aspx'
        # anynoums normal
        nor_url = 'https://proxy.coderbusy.com/zh-cn/classical/anonymous-type/anonymous/p{}.aspx'
        # high anynoums
        high_url = 'https://proxy.coderbusy.com/zh-cn/classical/anonymous-type/highanonymous/p{}.aspx'

        urls = []
        urls.extend([non_url.format(i) for i in range(pages + 1)])
        urls.extend([nor_url.format(i) for i in range(pages + 1)])
        urls.extend([high_url.format(i) for i in range(pages + 1)])
        for url in urls:
            tree = self.parse(url)
            if tree is None:
                continue
            for x in tree.xpath('//tbody/tr'):
                proxy = {}
                proxy['ip'] = ''.join(x.xpath('td[1]/text()')).strip()
                proxy['port'] = x.xpath('td[2]/text()')[0]
                proxy['location'] = x.xpath('td[3]/a/text()')
                elm = x.xpath('td[8]/span/text()')
                proxy['https'] = False if len(elm) == 0 else True
                anonymous = x.xpath('td[7]/text()')[0]
                proxy['anonymous'] = True if anonymous != '透明' else False
                yield proxy


if __name__ == '__main__':
    spider = CoderBusy()
    proxy = spider.get_proxy()
    for p in proxy:
        print(p)
