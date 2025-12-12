import scrapy

class CinemarkMoviesSpider(scrapy.Spider):
    name = "cinemark_movies"
    allowed_domains = ["cinemark-peru.com", "bff.cinemark-peru.com"]

    start_urls = [
        "https://bff.cinemark-peru.com/api/cinema/movies?theater=659"
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

        self.logger.info(f"Películas encontradas: {len(movies)}")

        for movie in movies:
            yield {
                "title": movie.get("title"),
                "slug": movie.get("slug"),
                "duration": movie.get("duration"),
                "rating": movie.get("rating"),
                "formats": movie.get("formats"),
            }
