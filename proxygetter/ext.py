import re

import pymongo
from pymongo import MongoClient

from proxygetter.utils import from_object


class ProxyDB:

    def __init__(self):
        client = MongoClient()
        db = client.spider
        self._proxies = db.proxies

    proxy_data = ('ip', 'port', 'https', 'anonymous', 'location', 'delay')  # 'validate'
    ip_pattern = re.compile(r'^([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$')

    def save(self, data):
        """Save on local mongodb
        kawrgs: to update the data
        Example: {
            'ip': '12.12.12.12',
            'port': 8000,
            'https': True,
            'anonymous': True,
            'location': '北京市',
            'delay': 3,
            # validate
        }
        """
        # update the proxy
        if self._proxies.find_one_and_delete({'ip': data['ip']}):
            return self._proxies.insert_one(data)

        proxy = {}
        for key in self.proxy_data:
            proxy[key] = data.get(key, None)

        if not proxy['ip'] and not self.ip_pattern.match(proxy['ip']):
            raise ProxyValueError
        try:
            if proxy['port']:
                proxy['port'] = int(proxy['port'])
            if proxy['delay']:
                proxy['delay'] = float(proxy['delay'])
        except Exception:
            raise
        if proxy['https'] not in (True, False):
            raise ProxyValueError('https')
        if proxy['anonymous'] not in (True, False):
            raise ProxyValueError('anonymous')

        return self._proxies.insert_one(data)

    def get(self, filter=None):
        return self._proxies.find_one(filter)

    def delete(self, proxy):
        self._proxies.delete_one(proxy)

    def find(self, filter):
        return self._proxies.find(filter, projection={'_id': False}, sort=[('validate_time', pymongo.DESCENDING)])

    def count(self):
        return self._proxies.count()

    def clear(self):
        self._proxies.delete_many({})


class ProxyValueError(Exception):
    """Wrong proxy value
    """


proxydb = ProxyDB()


class Setting:
    def __init__(self):
        from_object(self.__dict__, 'proxygetter.settings')


setting = Setting()
