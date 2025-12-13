"""
Spider para extraer funciones/horarios de Cinemark Peru
Optimizado para Zyte Scrapy Cloud
"""
import scrapy
from datetime import datetime, timedelta
from cinemark_project.items import ShowtimeItem


class CinemarkShowtimesSpider(scrapy.Spider):
    """
    Spider para extraer horarios de películas en todos los cines.
    
    Uso en Zyte Scrapy Cloud:
    - Ve a Jobs -> Run
    - Selecciona este spider: cinemark_showtimes
    - Opcional: Pasar argumento cinema_id para un cine específico
    """
    name = "cinemark_showtimes"
    
    custom_settings = {
        "FEEDS": {
            "showtimes.json": {
                "format": "json",
                "encoding": "utf-8",
                "indent": 2,
                "overwrite": True,
            }
        },
    }
    
    # URLs de las APIs
    THEATERS_API = "https://bff.cinemark-peru.com/api/cinema/theaters"
    SHOWTIMES_API = "https://bff.cinemark-peru.com/api/cinema/showtimes"
    
    def __init__(self, cinema_id=None, *args, **kwargs):
        """
        Args:
            cinema_id: ID específico de cine (opcional)
        """
        super().__init__(*args, **kwargs)
        self.target_cinema_id = cinema_id
    
    def start_requests(self):
        """Primero obtiene la lista de cines"""
        headers = {
            "accept": "application/json",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
            "country": "PE",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        yield scrapy.Request(
            url=self.THEATERS_API,
            headers=headers,
            callback=self.parse_theaters,
            meta={
                "zyte_api": {
                    "httpResponseBody": True,
                }
            }
        )
    
    def parse_theaters(self, response):
        """Procesa la lista de cines y solicita horarios para cada uno"""
        try:
            payload = response.json()
        except Exception as e:
            self.logger.error(f"Error parsing theaters JSON: {e}")
            return
        
        theaters = payload.get("data", [])
        self.logger.info(f"📍 Cines encontrados: {len(theaters)}")
        
        # Fecha de hoy para consultar horarios
        today = datetime.now().strftime("%Y-%m-%d")
        
        headers = {
            "accept": "application/json",
            "origin": "https://www.cinemark-peru.com",
            "referer": "https://www.cinemark-peru.com/",
            "country": "PE",
        }
        
        for theater in theaters:
            cinema_id = theater.get("cinemaId") or theater.get("id")
            
            # Si se especificó un cine específico, filtrar
            if self.target_cinema_id and str(cinema_id) != str(self.target_cinema_id):
                continue
            
            cinema_name = theater.get("name", "Unknown")
            
            # Construir URL para horarios de este cine
            url = f"{self.SHOWTIMES_API}?cinemaId={cinema_id}&date={today}"
            
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse_showtimes,
                meta={
                    "cinema_id": cinema_id,
                    "cinema_name": cinema_name,
                    "zyte_api": {
                        "httpResponseBody": True,
                    }
                }
            )
    
    def parse_showtimes(self, response):
        """Procesa los horarios de un cine específico"""
        cinema_id = response.meta["cinema_id"]
        cinema_name = response.meta["cinema_name"]
        
        try:
            payload = response.json()
        except Exception as e:
            self.logger.error(f"Error parsing showtimes JSON for {cinema_name}: {e}")
            return
        
        movies = payload.get("data", [])
        self.logger.info(f"🎬 {cinema_name}: {len(movies)} películas con horarios")
        
        for movie in movies:
            movie_id = movie.get("corporateId")
            movie_title = movie.get("title")
            
            # Cada película puede tener múltiples formatos/horarios
            showtimes = movie.get("showtimes") or []
            
            for showtime in showtimes:
                item = ShowtimeItem()
                
                item["movie_id"] = movie_id
                item["cinema_id"] = cinema_id
                item["date"] = showtime.get("date")
                item["time"] = showtime.get("time")
                item["format"] = showtime.get("format")
                item["language"] = showtime.get("language")
                item["purchase_url"] = showtime.get("purchaseUrl")
                
                yield item
