import scrapy

class CinemarkMoviesSpider(scrapy.Spider):
    name = "cinemark_movies"
    allowed_domains = ["bff.cinemark-peru.com"]

    start_urls = [
        "https://bff.cinemark-peru.com/api/cinema/movies?theater=659"
    ]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0",
        "DEFAULT_REQUEST_HEADERS": {
            "accept": "application/json, text/plain, */*",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
        },
    }

    def parse(self, response):
        data = response.json()

        movies = None
        if isinstance(data, list):
            movies = data
        elif isinstance(data, dict):
            for k in ("movies", "data", "items"):
                if isinstance(data.get(k), list):
                    movies = data[k]
                    break
            if not movies and isinstance(data.get("result"), dict):
                r = data["result"]
                for k in ("movies", "data", "items"):
                    if isinstance(r.get(k), list):
                        movies = r[k]
                        break

        if not movies:
            yield {"raw": data}
            return

        self.logger.info(f"Películas encontradas: {len(movies)}")

        for m in movies:
            slug = m.get("slug")
            item = {
                "id": m.get("id") or m.get("movieId"),
                "corporateId": m.get("movieCorporateId"),
                "title": m.get("title") or m.get("name"),
                "slug": slug,
                "rating": m.get("rating"),
                "runtime": m.get("runtime") or m.get("duration"),
                "releaseDate": m.get("releaseDate"),
            }
            yield item

            if slug:
                url = f"https://bff.cinemark-peru.com/api/cinema/movies/slug/{slug}"
                yield scrapy.Request(url, callback=self.parse_detail, meta={"basic": item})

    def parse_detail(self, response):
        basic = response.meta["basic"]
        d = response.json()

        yield {
            **basic,
            "synopsis": d.get("synopsis") or d.get("description"),
            "genres": d.get("genres"),
            "poster": d.get("poster") or d.get("image"),
            "trailer": d.get("trailer"),
        }
