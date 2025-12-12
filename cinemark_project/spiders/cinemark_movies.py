import scrapy

class CinemarkMoviesSpider(scrapy.Spider):
    name = "cinemark_movies"
    allowed_domains = ["bff.cinemark-peru.com"]

    start_urls = [
        "https://bff.cinemark-peru.com/api/cinema/movies"
    ]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.cinemark-peru.com",
            "Referer": "https://www.cinemark-peru.com/",
        }
    }

    def parse(self, response):
        data = response.json()

        movies = data if isinstance(data, list) else data.get("movies", [])

        for m in movies:
            yield {
                "title": m.get("title"),
                "slug": m.get("slug"),
                "duration": m.get("duration"),
                "rating": m.get("rating"),
                "formats": m.get("formats"),
                "poster": m.get("poster"),
            }
