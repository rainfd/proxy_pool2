import logging

# create logger
logging.basicConfig(filename='spider.log', filemode='a', level=logging.DEBUG)
logger = logging.getLogger('proxy_spider')
# logger.setLevel(logging.INFO)

logging.getLogger('requests').setLevel(logging.ERROR)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)
