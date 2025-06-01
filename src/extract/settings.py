# Scrapy settings for extract project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "extract"

SPIDER_MODULES = ["extract.spiders"]
NEWSPIDER_MODULE = "extract.spiders"

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
DOWNLOAD_DELAY = 10
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 540

ADDONS = {}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "extract (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SPIDERMON_ENABLED = True

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    #'spidermon.contrib.scrapy.extensions.SpiderMonitor': 500,
    #'spidermon.contrib.scrapy.extensions.SpiderStatsMonitor': 500,
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
    #'spidermon.contrib.extensions.SpiderMonitor': 500,
    
    #'extract.extensions.closespider.CloseSpider': 1
}

SPIDERMON_SPIDER_CLOSE_MONITORS = ( # works on all spiders or create a specific one for each spider
    #'extract.spiders.amazon.SpiderMonitor',
    'extract.monitors.SpiderCloseMonitorSuite',
    #'monitors.SpiderCloseMonitorSuite',
    #'extract.spiders.main.AmazonMonitorSuite',  # Corrected path

)

# Configure item pipelines
CUSTOM_MIN_STATUS_200 = 1
CUSTOM_MAX_STATUS_503 = 0
CUSTOM_MIN_ITEMS_SCRAPED = 350
SPIDERMON_MAX_ERRORS = 0


ITEM_PIPELINES = { #to able to use the schemas 
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 800,
}
SPIDERMON_VALIDATION_SCHEMAS = ("./ml-scraping/src/extract/schemas/amzn_item.json",)
# Path to your JSON schema
SPIDERMON_MAX_ITEM_VALIDATION_ERRORS = 0  # Maximum number of validation errors allowed per item



SPIDERMON_PERIODIC_MONITORS = {#to run periodically, e.g. every 3 seconds
    'extract.monitors.PeriodicExecutionTimeMonitor': 5, 
}
SPIDERMON_MAX_EXECUTION_TIME = 20



SPIDERMON_REPORT_TEMPLATE = "reports/email/monitors/result.jinja"
SPIDERMON_REPORT_CONTEXT = {
    'report_title': 'Amazon Spider Monitoring Report',
}
SPIDERMON_REPORT_FILENAME = "amzn_report2.html"


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br', # 'br' for brotli, 'gzip' for gzip compression
    'Referer': 'https://www.amazon.com.br/', # Mimic coming from Amazon itself
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "extract.middlewares.ExtractSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "extract.middlewares.ExtractDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "extract.pipelines.ExtractPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

HTTPERROR_ALLOWED_CODES = [503]
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
