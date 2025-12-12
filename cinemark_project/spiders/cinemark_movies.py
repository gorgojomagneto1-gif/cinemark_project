import scrapy

class CinemarkMoviesSpider(scrapy.Spider):
    name = "cinemark_movies"

    handle_httpstatus_list = [403]

    def __init__(self, theater="659", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theater = theater

    def start_requests(self):
        url = f"https://bff.cinemark-peru.com/api/cinema/movies?theater={self.theater}"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "country": "PE",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }

        yield scrapy.Request(url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        if response.status == 403:
            self.logger.error("403 body (primeros 300 chars): %s", response.text[:300])
            return

        data = response.json()

        movies = data.get("movies", data) if isinstance(data, dict) else data

        if not movies:
            yield {"raw": data}
            return

        self.logger.info(f"Películas encontradas: {len(movies)}")

        for m in movies:
            yield {
                "title": m.get("title"),
                "slug": m.get("slug"),
                "corporateId": m.get("corporateId") or m.get("id"),
                "rating": m.get("rating"),
                "runtime": m.get("runtime") or m.get("duration"),
            }
