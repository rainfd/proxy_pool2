import os
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from proxygetter.logger import logger
from proxygetter.ext import setting
from proxygetter.executor import ValidateRunner, CrawlRunner


scheduler = BlockingScheduler()

crawl = CrawlRunner()
validate = ValidateRunner()

scheduler.add_job(crawl.start, 'interval', seconds=setting.SPIDER_INTERVAL)
scheduler.add_job(validate.start, 'interval', seconds=setting.VALIDATE_INTERVAL, max_instances=20)
scheduler.add_job(validate.add_task, 'interval', seconds=setting.VALIDATE_ADD_INTERVAL)
# job = scheduler.add_job(lambda: print('TEST!!'), 'interval', seconds=5)


def beat():
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # validate.start()
        logger.info('Crawl once.')
        crawl.start()
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()


if __name__ == '__main__':
    beat()
