import scrapy
from scrapy import Field, Item


class MovieItem(Item):
    """Item para películas de Cinemark"""
    # Identificadores
    corporate_id = Field()
    slug = Field()
    
    # Información básica
    title = Field()
    original_title = Field()
    status = Field()  # NOW_SHOWING, COMING_SOON, PRESALE
    
    # Fechas
    opening_date = Field()
    
    # Duración y clasificación
    runtime = Field()  # en minutos
    rating = Field()  # clasificación de edad
    
    # Media
    poster_url = Field()
    trailer_url = Field()
    
    # Formatos y lenguajes
    formats = Field()  # lista: ['2D', '3D', 'XD', 'DBOX']
    languages = Field()  # lista: ['ESP', 'SUB']
    
    # Detalles adicionales (del detalle de película)
    synopsis = Field()
    director = Field()
    cast = Field()
    genre = Field()
    distributor = Field()


class TheaterItem(Item):
    """Item para cines de Cinemark"""
    cinema_id = Field()
    name = Field()
    slug = Field()
    address = Field()
    city = Field()
    
    # Formatos disponibles
    available_formats = Field()  # lista: ['2D', '3D', 'XD', 'DBOX']
    
    # Coordenadas (si disponibles)
    latitude = Field()
    longitude = Field()


class ShowtimeItem(Item):
    """Item para funciones/horarios"""
    movie_id = Field()
    cinema_id = Field()
    
    date = Field()
    time = Field()
    
    format = Field()  # 2D, 3D, XD, etc.
    language = Field()
    
    purchase_url = Field()
