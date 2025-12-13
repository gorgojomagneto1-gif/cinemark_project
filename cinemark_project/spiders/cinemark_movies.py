import json
import scrapy
from cinemark_project.items import MovieItem

class CinemarkMoviesSpider(scrapy.Spider):
    name = "cinemark_movies"
    allowed_domains = ["bff.cinemark-peru.com"]

    custom_settings = {
        "FEEDS": {
            "movies.json": {
                "format": "json",
                "encoding": "utf-8",
                "indent": 2,
                "overwrite": True,
            }
        },
    }

    def __init__(self, theater=None, status=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theater = theater  # ej: 659 (opcional)
        self.status = status    # ej: SHOWING_NOW / COMING_SOON / PRESALE (opcional)

    def start_requests(self):
        url = "https://bff.cinemark-peru.com/api/cinema/movies"
        if self.theater:
            url += f"?theater={self.theater}"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
            "country": "PE",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        # dont_filter=True para evitar que Scrapy bloquee reintentos o duplicados si la URL es igual
        yield scrapy.Request(url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            data = response.json()
        except json.JSONDecodeError:
            self.logger.error("Error decoding JSON response")
            return

        movies = data.get("data", [])
        self.logger.info(f"Peliculas encontradas: {len(movies)}")

        for m in movies:
            # Filtro opcional por status (si se pasó argumento)
            if self.status and m.get("status") != self.status:
                continue

            item = MovieItem()
            item["title"] = m.get("title")
            item["slug"] = m.get("slug")
            item["corporate_id"] = m.get("corporateId")
            item["status"] = m.get("status")
            item["opening_date"] = m.get("openingDate")
            item["runtime"] = m.get("runTime")
            item["rating"] = m.get("rating")
            item["poster_url"] = m.get("posterUrl")
            item["formats"] = [f.get("shortName") for f in (m.get("formats") or [])]
            item["languages"] = [l.get("shortName") for l in (m.get("languages") or [])]
            
            yield item
