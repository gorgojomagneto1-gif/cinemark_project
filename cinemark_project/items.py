import scrapy

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    slug = scrapy.Field()
    duration = scrapy.Field()
    rating = scrapy.Field()
    formats = scrapy.Field()
    poster = scrapy.Field()
