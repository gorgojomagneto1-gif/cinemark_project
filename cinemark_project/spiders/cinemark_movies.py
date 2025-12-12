import scrapy

class CinemarkMoviesSpider(scrapy.Spider):
    name = "cinemark_movies"

    custom_settings = {
        "FEEDS": {"movies.json": {"format": "json", "indent": 2}},
    }

    def start_requests(self):
        url = "https://bff.cinemark-peru.com/api/cinema/movies"
        headers = {
            "accept": "application/json",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
            "country": "PE",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        payload = response.json()
        movies = payload.get("data", [])
        
        self.logger.info(f"Películas encontradas: {len(movies)}")
        
        for m in movies:
            yield {
                "corporateId": m.get("corporateId"),
                "slug": m.get("slug"),
                "title": m.get("title"),
                "status": m.get("status"),
                "openingDate": m.get("openingDate"),
                "runTime": m.get("runTime"),
                "rating": m.get("rating"),
                "posterUrl": m.get("posterUrl"),
                "formats": [f.get("shortName") for f in (m.get("formats") or [])],
                "languages": [l.get("shortName") for l in (m.get("languages") or [])],
            }
