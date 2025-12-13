"""
Spider principal para extraer películas de Cinemark Peru
Optimizado para Zyte Scrapy Cloud
"""
import scrapy
from scrapy_zyte_api import ZyteApiResponse
from cinemark_project.items import MovieItem


class CinemarkMoviesSpider(scrapy.Spider):
    """
    Spider para extraer todas las películas de Cinemark Peru.
    
    Uso en Zyte Scrapy Cloud:
    - Ve a Jobs -> Run
    - Selecciona este spider: cinemark_movies
    - Los resultados se guardan automáticamente en Items
    """
    name = "cinemark_movies"
    
    # Configuración del spider
    custom_settings = {
        # Output en JSON al correr localmente
        "FEEDS": {
            "movies.json": {
                "format": "json",
                "encoding": "utf-8",
                "indent": 2,
                "overwrite": True,
            }
        },
    }
    
    # URL de la API de Cinemark Peru (es una API pública)
    API_URL = "https://bff.cinemark-peru.com/api/cinema/movies"
    
    def start_requests(self):
        """Inicia la solicitud a la API de películas"""
        headers = {
            "accept": "application/json",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
            "country": "PE",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        
        yield scrapy.Request(
            url=self.API_URL,
            headers=headers,
            callback=self.parse,
            meta={
                # Configuración específica para Zyte API
                "zyte_api": {
                    "httpResponseBody": True,
                    "httpResponseHeaders": True,
                }
            }
        )
    
    def parse(self, response):
        """Procesa la respuesta de la API de películas"""
        try:
            payload = response.json()
        except Exception as e:
            self.logger.error(f"Error parsing JSON: {e}")
            return
        
        movies = payload.get("data", [])
        self.logger.info(f"✅ Películas encontradas: {len(movies)}")
        
        for movie in movies:
            item = MovieItem()
            
            # Identificadores
            item["corporate_id"] = movie.get("corporateId")
            item["slug"] = movie.get("slug")
            
            # Información básica
            item["title"] = movie.get("title")
            item["original_title"] = movie.get("originalTitle")
            item["status"] = movie.get("status")  # NOW_SHOWING, COMING_SOON, PRESALE
            
            # Fechas
            item["opening_date"] = movie.get("openingDate")
            
            # Duración y clasificación
            item["runtime"] = movie.get("runTime")
            item["rating"] = movie.get("rating")
            
            # Media
            item["poster_url"] = movie.get("posterUrl")
            item["trailer_url"] = movie.get("trailerUrl")
            
            # Formatos y lenguajes
            formats = movie.get("formats") or []
            item["formats"] = [f.get("shortName") for f in formats if f.get("shortName")]
            
            languages = movie.get("languages") or []
            item["languages"] = [l.get("shortName") for l in languages if l.get("shortName")]
            
            # Detalles adicionales
            item["synopsis"] = movie.get("synopsis")
            item["genre"] = movie.get("genre")
            item["distributor"] = movie.get("distributor")
            
            # Cast y director (puede venir como lista o string)
            cast = movie.get("cast")
            if isinstance(cast, list):
                item["cast"] = [c.get("name") for c in cast if c.get("name")]
            else:
                item["cast"] = cast
                
            item["director"] = movie.get("director")
            
            yield item
