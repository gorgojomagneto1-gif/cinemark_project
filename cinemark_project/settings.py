BOT_NAME = "cinemark_project"

SPIDER_MODULES = ["cinemark_project.spiders"]
NEWSPIDER_MODULE = "cinemark_project.spiders"

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
