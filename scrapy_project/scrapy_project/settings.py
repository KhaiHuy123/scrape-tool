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

# --------------------------- Override the default request headers: --------------------------- #
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# ---------------------------Fake user agent & rotate proxy --------------------------- #
#SCRAPEOPS_API_KEY = '20e9292e-fd6d-4fc1-8b0c-17a99fae2f5c'
#SCRAPEOPS_API_KEY = 'ce192c1d-8164-4ff8-bec5-406caab947e5'
SCRAPEOPS_API_KEY = '0a06c182-96ab-4eb8-8d94-3e640f06e7bb'
SCRAPROPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPROPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

#SCRAPEOPS_CURL_X_COMMAND : 'https://proxy.scrapeops.io/v1/?api_key=Y20e9292e-fd6d-4fc1-8b0c-17a99fae2f5c&url'
#SCRAPERAPI_CURL_X_COMMAND : "http://scraperapi:4505a4f35383711d43debabd75d2e148@proxy-server.scraperapi.com:8001"

SCRAPERAPI_PROXY_PARAMS = [
    ['scraperapi', 'proxy-server.scraperapi.com:8001', '67ffab08154296f41b13d17021872c7f'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '1e8bad5dca50612f6cbbf5e76cb41358'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '29b3b8edc46f3b4b6d2e620e01d6c19c'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '3b0100de75c46a0bbcd541d1b5027847'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '3c61b1bc72ed3df21add1475f585c2de'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '9c7fb8da0711e472484b601692891728'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '6a20c3c503c77c50ecf17782942ad911'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '7a63e41562f6929273409e761f013342'],
    # ['scraperapi', 'proxy-server.scraperapi.com:8001', '32c1affc526a22f4266837ef5ed241f0']
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
   "scrapy_project.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware":400,
   "scrapy_project.middlewares.RotateProxyMiddleware":600,
}

# --------------------------- Enable or disable extensions --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# --------------------------- Configure item pipelines --------------------------- #
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #"scrapy_project.pipelines.ScrapyProjectPipeline" : 300,
   #"scrapy_project.pipelines.AmazonPipeline" : 300,
   "scrapy_project.pipelines.FahasaPipeline" : 300,
   #"scrapy_project.pipelines.FahasaListPipeline" : 300,
   #"scrapy_project.pipelines.NettruyenPipeLine" : 300,
   #"scrapy_project.pipelines.TruyenqqiPipeline" : 300,
   #"scrapy_project.pipelines.TheSunPipeline" : 300,
   #"scrapy_project.pipelines.DailyMailPipeline" : 300,
   #"scrapy_project.pipelines.Saveto_sqlServerNettruyenPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerTruyenqqiPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerAmazonPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerFahasaPipeline" : 400,
   #"scrapy_project.pipelines.Saveto_sqlServerFahasaPipeline_finalstate": 550,
   #"scrapy_project.pipelines.Saveto_sqlServerFahasaListPipeline" : 400,
   "scrapy_project.pipelines.FileWriterPipeline" : 350
}

# --------------------------- Parameters of Saveto_sqlServerPipeline --------------------------- #
SQL_SERVER = 'DESKTOP-LMGN073\SQLEXPRESS'
#SQL_DATABASE = 'manga'
#SQL_DATABASE = 'manga_nettruyen'
#SQL_DATABASE = 'manga_truyenqqi'
SQL_DATABASE = 'online_books'
#SQL_DATABASE = 'product_web_scraping'
#SQL_PASSWORD = 'password' # No need if using local database engine DBSM
SQL_AUTHENTICATION = 'Trusted_Connection=yes'
SQL_USERNAME = 'DESKTOP-LMGN073\HTH'

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