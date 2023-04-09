# telegram-python-es

Publicación de eventos de Meetup de la comunidad de Python España en Telegram.

Notas: <https://hackmd.io/@juanlu/r1ZnVlgzh>

## Github Actions

El fichero `.github/workflows/publish.yml` indica cada cuánto tiempo se ejecuta el cron de ejecución, el cual
obtiene de las comunidades de Meetup los últimos eventos y los publica en Telegram.

El estado de las últimas ejecuciones puede verificarse en el siguiente enlace:
<https://github.com/PyCampES/telegram-python-es/actions/runs/>

El punto de entrada (`main.py`) recibe una variable de entorno `MEETUP_SECRET`, la cual se configura a través del
enlace <https://github.com/PyCampES/telegram-python-es/settings/secrets/actions> .
