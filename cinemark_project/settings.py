# Scrapy settings for cinemark_project project
#
# Configurado para Zyte Scrapy Cloud

BOT_NAME = "cinemark_project"

SPIDER_MODULES = ["cinemark_project.spiders"]
NEWSPIDER_MODULE = "cinemark_project.spiders"

# Crawl responsibly
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure a delay for requests (in seconds)
DOWNLOAD_DELAY = 0.5

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
}

# Configure item pipelines
# ITEM_PIPELINES = {
#    "cinemark_project.pipelines.CinemarkProjectPipeline": 300,
# }

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# ==============================================================================
# ZYTE API CONFIGURATION
# ==============================================================================
# These settings enable scrapy-zyte-api integration
# The API key will be read from ZYTE_API_KEY environment variable in Scrapy Cloud

# Download handler for Zyte API
DOWNLOAD_HANDLERS = {
    "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
    "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
}

# Zyte API settings
ZYTE_API_TRANSPARENT_MODE = True  # Makes all requests go through Zyte API automatically
ZYTE_API_ENABLED = True

# Retry configuration for Zyte API
ZYTE_API_RETRY_POLICY = "scrapy_zyte_api.retry.aggressive_retry_policy"

# Logging
LOG_LEVEL = "INFO"
