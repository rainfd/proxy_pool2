import logging
import logging.handlers

# create logger
logging.basicConfig(level=logging.DEBUG)
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

fh = logging.handlers.TimedRotatingFileHandler(
    './logs/proxy_spider', 'S', 1, 30, encoding='utf-8', utc=True)
fh.suffix = "%Y%m%d.log"

fh.setFormatter(formatter)

logger.addHandler(fh)
