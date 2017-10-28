import logging
from datetime import datetime, timedelta
from random import randint
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from proxygetter.logger import logger
from proxygetter.ext import proxydb, setting
from proxygetter.utils import import_string
from proxygetter.proxyspider import ProxySpider

RELAXED_SIZE = 10
HEAVILY_SIZE = 80

proxy_queue = Queue()


class ValidateRunner:

    def start(self):
        proxy = proxy_queue.get()
        if proxy:
            self.validate(proxy)

    def add_task(self, proxy=None):
        if proxy is None:
            if 0 < proxy_queue.qsize() < RELAXED_SIZE:
                num = randint(0, proxydb.count() - 1)
                proxy = proxydb.find()[num]
            else:
                return
        proxy_queue.put(proxy)

    def validate(self, proxy):
        delay = ProxySpider.validate(proxy)
        if delay:
            proxy['delay'] = delay
            dt = datetime.now() + timedelta(hours=8)
            proxy['validate_time'] = dt.strftime('%Y/%m/%d %H:%M')
            proxydb.save(proxy)
            logger.debug('proxy: {}'.format(proxy))
            logger.debug('Update/Save a proxy')
        else:
            proxydb.delete(proxy)
            logger.debug('Delete a proxy')


class CrawlRunner:

    def __init__(self):
        self._spider_modules = self._spdier_loader()

    def _spdier_loader(self):
        spiders = {}
        for module, interval in setting.SPIDER_MODULES.items():
            mod = import_string('proxygetter.spiders.' + module)
            spiders[mod] = interval

        return spiders

    def crawl(self):
        # thread_workers = setting.THREAD_WORKERS

        def worker(spider, interval):
            sp = spider(interval)
            for proxy in sp.get_proxy():
                proxy_queue.put(proxy)

        for spider, interval in self._spider_modules.items():
            worker(spider, interval)

    def start(self):
        self.crawl()

    def pause(self):
        pass

    def continure(self):
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    # runner = CrawlRunner()
    # runner.crawl()
    pass
    runner = ValidateRunner()
    cr = CrawlRunner()
    cr.crawl()
    runner.start()
