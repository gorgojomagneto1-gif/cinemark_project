# ==============================================================================
# 🎬 CINEMARK PERU SCRAPER - ZYTE SCRAPY CLOUD
# ==============================================================================
# Proyecto configurado para deploy en Zyte Scrapy Cloud

## 📋 Requisitos

1. Cuenta en [Zyte](https://app.zyte.com/) (tienen $5 gratis de prueba)
2. Python 3.9+ instalado
3. Git instalado

## 🚀 Pasos para Deploy en Zyte

### 1. Conectar GitHub con Zyte

1. Ve a [app.zyte.com](https://app.zyte.com/)
2. Crea un nuevo proyecto de Scrapy Cloud
3. Ve a **Code & Deploys** → **Connect to GitHub**
4. Autoriza y selecciona el repositorio `cinemark_project`
5. Selecciona la rama `master`

### 2. Configurar el Project ID

1. Una vez creado el proyecto, copia el **Project ID** de la URL:
   ```
   https://app.zyte.com/p/YOUR_PROJECT_ID/...
   ```
2. Edita el archivo `scrapinghub.yml` y reemplaza `YOUR_PROJECT_ID` con tu ID

### 3. Configurar API Key de Zyte

En Zyte Scrapy Cloud, la API key se configura automáticamente.
Si necesitas configurarla manualmente:

1. Ve a **Settings** → **API Access**
2. Copia tu API key
3. En **Job Settings**, agrega la variable:
   ```
   ZYTE_API_KEY=tu_api_key_aqui
   ```

### 4. Deploy Automático

Una vez conectado GitHub:
- Cada push a `master` desplegará automáticamente
- O puedes hacer deploy manual desde **Code & Deploys**

## 🕷️ Spiders Disponibles

| Spider | Descripción | Comando |
|--------|-------------|---------|
| `cinemark_movies` | Todas las películas | `scrapy crawl cinemark_movies` |

### Argumentos del Spider (Movies)

Puedes filtrar los resultados pasando argumentos:

- **Por Cine**: `theater=659` (ID del cine)
- **Por Estado**: `status=SHOWING_NOW` (o `COMING_SOON`, `PRESALE`)

**Ejemplo local:**
```bash
scrapy crawl cinemark_movies -a theater=659 -a status=SHOWING_NOW
```

**Ejemplo en Zyte (Arguments):**
```text
theater=659
status=SHOWING_NOW
```
| `cinemark_theaters` | Todos los cines | `scrapy crawl cinemark_theaters` |
| `cinemark_showtimes` | Horarios de funciones | `scrapy crawl cinemark_showtimes` |

## ▶️ Ejecutar en Zyte Scrapy Cloud

1. Ve a tu proyecto en Zyte
2. Click en **Jobs** → **Run**
3. Selecciona el spider que quieres ejecutar
4. Click en **Run**
5. Los resultados aparecerán en la pestaña **Items**

## 💻 Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar spider localmente
scrapy crawl cinemark_movies

# Los resultados se guardan en movies.json
```

## 📁 Estructura del Proyecto

```
cinemark_project/
├── scrapy.cfg              # Configuración de Scrapy
├── scrapinghub.yml         # Configuración de Zyte Scrapy Cloud
├── requirements.txt        # Dependencias Python
├── README.md               # Este archivo
└── cinemark_project/
    ├── __init__.py
    ├── items.py            # Modelos de datos
    ├── settings.py         # Configuración (con Zyte API)
    └── spiders/
        ├── __init__.py
        ├── cinemark_movies.py      # Spider de películas
        ├── cinemark_theaters.py    # Spider de cines
        └── cinemark_showtimes.py   # Spider de horarios
```

## 📊 Datos Extraídos

### Películas (MovieItem)
- `title`, `original_title`, `slug`
- `status` (NOW_SHOWING, COMING_SOON, PRESALE)
- `runtime`, `rating`, `opening_date`
- `poster_url`, `trailer_url`
- `formats` (2D, 3D, XD, DBOX)
- `languages` (ESP, SUB)
- `synopsis`, `director`, `cast`, `genre`

### Cines (TheaterItem)
- `name`, `slug`, `cinema_id`
- `address`, `city`
- `available_formats`
- `latitude`, `longitude`

### Horarios (ShowtimeItem)
- `movie_id`, `cinema_id`
- `date`, `time`
- `format`, `language`
- `purchase_url`

## ⚠️ Notas Importantes

- El sitio web de Cinemark usa una API interna que devuelve JSON
- Los spiders están optimizados para usar Zyte API como proxy
- Respeta los términos de servicio del sitio web
