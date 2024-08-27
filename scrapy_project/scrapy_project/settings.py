# Scrapy settings for scrapy_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrapy_project"
SPIDER_MODULES = ["scrapy_project.spiders"]
NEWSPIDER_MODULE = "scrapy_project.spiders"

# ------------------------- Crawl responsibly by identifying yourself (and your website) on the user-agent --------------------------- #
#USER_AGENT = "scrapy_project (+http://www.yourdomain.com)"
#USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.864.75"
#USER_AGENT ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'

# ------------------------- Obey robots.txt rules --------------------------- #
#ROBOTSTXT_OBEY = False
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# --------------------------- See also autothrottle settings and docs --------------------------- #
DOWNLOAD_DELAY = 8
# --------------------------- The download delay setting will honor only one of: --------------------------- #
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# --------------------------- Disable cookies (enabled by default) --------------------------- #
#COOKIES_ENABLED = False

# --------------------------- Disable Telnet Console (enabled by default) --------------------------- #
#TELNETCONSOLE_ENABLED = False
#TELNETCONSOLE_ENABLED = True
#TELNETCONSOLE_PASSWORD = ''
#TELNETCONSOLE_PORT = [6023,6073]

# --------------------------- Override the default request headers: --------------------------- #
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# ---------------------------Fake user agent & rotate proxy --------------------------- #
SCRAPEOPS_API_KEY = ''
SCRAPROPS_FAKE_USER_AGENT_ENDPOINT = ''
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPROPS_FAKE_BROWSER_HEADER_ENDPOINT = ''
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

SCRAPERAPI_PROXY_PARAMS = [
    # ['user_name', 'proxy_end_point', 'api_key']
    # Add more
]

PROXY_API_KEY = ''
PROXY_USER = ''
PROXY_PASSWORD = ''
PROXY_ENDPOINT = ''
PROXY_PORT = ''

# --------------------------- Time out for response --------------------------- #
#DOWNLOAD_TIMEOUT = 180

# --------------------------- Enable or disable spider middlewares --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "scrapy_project.middlewares.ScrapyProjectSpiderMiddleware": 543,
}

# --------------------------- Enable or disable downloader middlewares --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "scrapy_project.middlewares.ScrapyProjectDownloaderMiddleware": 543,
   #"scrapy_project.middlewares.ScrapeOpsFakeUserAgentMiddleware":400,
   "scrapy_project.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 400,
   "scrapy_project.middlewares.RotateProxyMiddleware": 600,
}

# --------------------------- Enable or disable extensions --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# --------------------------- Configure item pipelines --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "scrapy_project.pipelines.ScrapyProjectPipeline" : 300,
   #"scrapy_project.pipelines.AmazonPipeline" : 300,
   #"scrapy_project.pipelines.FahasaPipeline" : 300,
   "scrapy_project.pipelines.FahasaListPipeline" : 300,
   #"scrapy_project.pipelines.NettruyenPipeLine" : 300,
   #"scrapy_project.pipelines.TruyenqqiPipeline" : 300,
   #"scrapy_project.pipelines.TheSunPipeline" : 300,
   #"scrapy_project.pipelines.DailyMailPipeline" : 300,
   #"scrapy_project.pipelines.Saveto_sqlServerNettruyenPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerTruyenqqiPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerAmazonPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerFahasaPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerFahasaPipeline_finalstate" : 550,
   "scrapy_project.pipelines.Saveto_sqlServerFahasaListPipeline" : 400,
   "scrapy_project.pipelines.FileWriterPipeline" : 350
}

# --------------------------- Parameters of Saveto_sqlServerPipeline --------------------------- #
SQL_SERVER = ''
#SQL_DATABASE = 'manga'
#SQL_DATABASE = 'manga_nettruyen'
#SQL_DATABASE = 'manga_truyenqqi'
SQL_DATABASE = 'online_books'
#SQL_DATABASE = 'db_bookstore'
#SQL_PASSWORD = 'password' # No need if using local database engine DBSM
SQL_AUTHENTICATION = 'Trusted_Connection=yes'
SQL_USERNAME = ''

# --------------------------- Stored data in flat file (csv) --------------------------- #
#FEEDS = {
#    'referance.csv' :{'format' : 'csv', 'overwrite' : True, 'encoding': 'utf-8-sig'}
# }

# --------------------------- RETRY --------------------------- #
RETRY_HTTP_CODES = [499]  # Retry for "499" status code
handle_httpstatus_list = [500]

# --------------------------- REDIRECT --------------------------- #
REDIRECT_ENABLED = True
HTTPERROR_ALLOWED_CODES = [301]
HTTPERROR_ALLOW_ALL = True

# --------------------------- Enable and configure the AutoThrottle extension (disabled by default) --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# --------------------------- Enable and configure HTTP caching (disabled by default) --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# --------------------------- Set settings whose default value is deprecated to a future-proof value --------------------------- #
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
