# telegram-python-es

Publicación de eventos de Meetup de la comunidad de Python España en Telegram.

## Extracción

Participantes:
- Alex
- Juanlu
- Nacho

Ideas:
- RSS? :x: 
  - Requiere estar logueado :scream: https://www.meetup.com/pydata-madrid/events/rss/
  - Más información https://github.com/OpenTwinCities/site_bot/issues/10
- iCAL? :x: 
  - Requiere estar logueado :scream: https://www.meetup.com/pydata-madrid/events/rss/
- GraphQL :arrow_backward: 
  - Pedido token de Meetup Pro :hourglass_flowing_sand: 
- Scraping????? OMG WOW

### Campos de GraphQL

- Documentación: https://www.meetup.com/api/schema/#Event
- Petición del token: https://www.meetup.com/api/authentication/#p04-jwt-flow-section

```
id
title
eventUrl
description
shortDescription
group
  id
  name
isOnline
eventType
venue
  id
  name
  address
  city
  postalCode
  lng
  lat
onlineVenue
  url
dateTime
duration
timezone
endTime
```

### Autenticación

Ayuda ChatGPT:

> act like you're an excellent Python programmer, that writes clean and effective code. write a complete OAuth2 authentication flow for the Meetup.com API, including requesting a JWT token, in Python.

Sure, here's an example OAuth2 authentication flow for the Meetup.com API in Python using the requests library:

```python
import requests

# Define Meetup.com API endpoint and credentials
MEETUP_API_ENDPOINT = 'https://api.meetup.com'
CLIENT_ID = '<YOUR_CLIENT_ID>'
CLIENT_SECRET = '<YOUR_CLIENT_SECRET>'
REDIRECT_URI = '<YOUR_REDIRECT_URI>'

# Define Meetup.com API OAuth2 URLs
AUTHORIZE_URL = 'https://secure.meetup.com/oauth2/authorize'
TOKEN_URL = 'https://secure.meetup.com/oauth2/access'

# Define scope for Meetup.com API
SCOPE = 'ageless'

# Define function to initiate OAuth2 authentication flow
def authenticate():
    # Redirect user to Meetup.com authorization page to get authorization code
    auth_params = {'client_id': CLIENT_ID, 'response_type': 'code', 'redirect_uri': REDIRECT_URI, 'scope': SCOPE}
    auth_response = requests.get(AUTHORIZE_URL, params=auth_params)
    authorization_code = input("Please enter the authorization code: ")
    
    # Exchange authorization code for access token
    token_params = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'code': authorization_code, 'redirect_uri': REDIRECT_URI, 'grant_type': 'authorization_code'}
    token_response = requests.post(TOKEN_URL, params=token_params)
    access_token = token_response.json()['access_token']
    
    # Get JWT token for API requests
    jwt_params = {'access_token': access_token}
    jwt_response = requests.post(f'{MEETUP_API_ENDPOINT}/oauth2/jwt', params=jwt_params)
    jwt_token = jwt_response.json()['token']
    
    # Return JWT token for API requests
    return jwt_token
```

This code defines the Meetup.com API endpoint and credentials, the OAuth2 URLs, and the scope for the API. It also defines a `authenticate()` function that initiates the OAuth2 authentication flow.

The `authenticate()` function redirects the user to the Meetup.com authorization page to get an authorization code, which is then exchanged for an access token. The access token is used to get a JWT token for API requests.

Note that you'll need to replace `<YOUR_CLIENT_ID>`, `<YOUR_CLIENT_SECRET>`, and `<YOUR_REDIRECT_URI>` with your own Meetup.com API credentials and redirect URI, respectively. You'll also need to customize the SCOPE variable to match your API requirements.

### Almacenamiento

- Hay que listar qué comunidades extraer
- **1 fichero `.json` por comunidad**

```json
```

## Infraestructura

Participantes:
- Nekmo
- Inna :eyes: 
- Unai :eyes: 
- Johanna :eyes: 

Ideas:
- Hace falta persistencia?
  - Pareciera que sí
  - Incluso por RSS hay que saber qué eventos ya se han consumido
- **GitHub Actions + cron?**
  - Guardar datos en archivos JSON
- AWS Lambda?
- PythonAnywhere?

### Github Actions

El fichero `.github/workflows/publish.yml` indica cada cuánto tiempo se ejecuta el cron de ejecución, el cual
obtiene de las comunidades de Meetup los últimos eventos y los publica en Telegram.

El estado de las últimas ejecuciones puede verificarse en el siguiente enlace:
<https://github.com/PyCampES/telegram-python-es/actions/runs/>

El punto de entrada (`main.py`) recibe una variable de entorno `MEETUP_SECRET`, la cual se configura a través del
enlace <https://github.com/PyCampES/telegram-python-es/settings/secrets/actions> .

## Publicación

Participantes:
- Sergio
- Ángel :eyes: 
- Jordi :eyes: 
- David :eyes: 

Ideas:
- Bot de Telegram
  - No tiene que estar en ejecución siempre
  - También a través de GitHub Actions
- Información
  - Nombre de Comunidad
  - Título
  - Fecha y hora RFC 3339
  - Sede/Lugar/Localización (LonLat + Nombre + Calle ???)
  - Breve descripción
  - Link directo al evento

## Retros

### Sprint 1

- Extracción
  - Está muy mal
  - Hemos aprendido `httpx`
  - La autenticación es un asco
  - Hay que hacer OAUTH2
  - ¿Cómo se hace en GitHub Actions?
  - ¿Es obligatorio hacerlo manualmente al principio?
- Guardado de archivos
  - Ya está el listado de comunidades
  - El resto está por hacer
- Infraestructura
  - Los secrets ya están funcionando
  - Había problemas con los repository secrets, tal vez se puede hacer funcionar
  - Hay una rama huérfana `events`
  - Explorar la posibilidad de simplificarlo
  - Se podría usar para separar un entorno de producción de uno de pruebas
  - Hay un PR que convierte todo en un paquete Python https://github.com/PyCampES/telegram-python-es/pull/4 pendiente de revisión
  - Con Black
  - Hacían falta `__init__.py` https://peps.python.org/pep-0420/
- Telegram
  - Bastante bien
  - Está hecho el modelo de eventos y se puede crear el mensaje que va al grupo
  - Queda el detalle del tema de la hora
  - Se podría cambiar la URL de Telegram a una constante
  - Faltan las credenciales del bot: ID y CHANNEL_ID
  - Se podrían tener 2 CHANNEL_ID
