# THREAD_WORKERS = 2

SPIDER_MODULES = {
    # spider_name: interval
    'coderbusy.CoderBusy': 1,
    # 'kuaidaili.KDLSpider': 1,
}

# 1 hour
SPIDER_INTERVAL = 60 * 60

# 5s
VALIDATE_INTERVAL = 5

# 20s
VALIDATE_ADD_INTERVAL = 20


"""
uri = "mongodb://%s:%s@%s" % (
    quote_plus(user), quote_plus(password), host)
"""
