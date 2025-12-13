"""
Spider para extraer información de cines de Cinemark Peru
Optimizado para Zyte Scrapy Cloud
"""
import scrapy
from cinemark_project.items import TheaterItem


class CinemarkTheatersSpider(scrapy.Spider):
    """
    Spider para extraer todos los cines de Cinemark Peru.
    
    Uso en Zyte Scrapy Cloud:
    - Ve a Jobs -> Run
    - Selecciona este spider: cinemark_theaters
    """
    name = "cinemark_theaters"
    
    custom_settings = {
        "FEEDS": {
            "theaters.json": {
                "format": "json",
                "encoding": "utf-8",
                "indent": 2,
                "overwrite": True,
            }
        },
    }
    
    # URL de la API de cines
    API_URL = "https://bff.cinemark-peru.com/api/cinema/theaters"
    
    def start_requests(self):
        """Inicia la solicitud a la API de cines"""
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
                "zyte_api": {
                    "httpResponseBody": True,
                    "httpResponseHeaders": True,
                }
            }
        )
    
    def parse(self, response):
        """Procesa la respuesta de la API de cines"""
        try:
            payload = response.json()
        except Exception as e:
            self.logger.error(f"Error parsing JSON: {e}")
            return
        
        theaters = payload.get("data", [])
        self.logger.info(f"✅ Cines encontrados: {len(theaters)}")
        
        for theater in theaters:
            item = TheaterItem()
            
            item["cinema_id"] = theater.get("cinemaId") or theater.get("id")
            item["name"] = theater.get("name")
            item["slug"] = theater.get("slug")
            item["address"] = theater.get("address")
            item["city"] = theater.get("city")
            
            # Formatos disponibles
            formats = theater.get("formats") or []
            item["available_formats"] = [f.get("shortName") for f in formats if f.get("shortName")]
            
            # Coordenadas
            item["latitude"] = theater.get("latitude")
            item["longitude"] = theater.get("longitude")
            
            yield item
