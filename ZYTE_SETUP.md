# Guía de Configuración Zyte (Gratis)

El proyecto está listo para Zyte, pero necesitas una cuenta. No te preocupes, tienen un plan gratuito ("Free Trial") que te da $5 de crédito, suficiente para probar todo esto.

## Paso 1: Crear Cuenta Gratuita
1. Ve a [https://app.zyte.com/account/signup/zyteapi](https://app.zyte.com/account/signup/zyteapi).
2. Regístrate con Google o Email.
3. Se creará automáticamente una "Organization" y un Proyecto por defecto.

## Paso 2: Obtener tus Credenciales

### Project ID
1. En el dashboard de Zyte, mira la URL de tu navegador.
2. Será algo como: `https://app.zyte.com/p/123456/jobs...`
3. El número `123456` es tu **Project ID**.

### API Key
1. En el menú izquierdo, ve a **Settings** -> **API Access**.
2. Copia la clave que aparece ahí.

## Paso 3: Configurar el Proyecto

1. Abre el archivo `scrapinghub.yml` en este proyecto.
2. Descomenta la línea `project` y pon tu número:
   ```yaml
   project: 123456
   ```

## Paso 4: Ejecutar Localmente (Opcional)

Si prefieres probar en tu PC antes de subir a la nube:

1. Crea un archivo `.env` (usa `.env.example` como base).
2. Pega tu API Key: `ZYTE_API_KEY=tu_clave_aqui`.
3. Ejecuta:
   ```bash
   scrapy crawl cinemark_movies
   ```
