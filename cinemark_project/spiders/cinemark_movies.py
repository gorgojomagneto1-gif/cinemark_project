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

        movies = data.get("result", {}).get("movies", [])

        for movie in movies:
            yield {
                "title": movie.get("title"),
                "slug": movie.get("slug"),
                "rating": movie.get("rating"),
                "duration": movie.get("duration"),
                "formats": movie.get("formats"),
                "poster": movie.get("poster"),
            }
