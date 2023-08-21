# Y_LAB_MENU_APP
API для ресторана на основе Fastapi, SQLAlchemy, PostgreSQL, Redis, Celery и Docker, созданный во время обучения на YLab University
## Запуск и тесты
Для запуска приложения с тестами (pytest) корневой директории в консоли выполнить:<br>
`docker-compose up -d`<br>
Когда все контейнеры (uvicorn server, postgres db, reddis, tests) запустятся, можно запустить тесты командой:<br>
`docker exec crud_tests pytest --color=yes -s -v /app/tests`<br>
(предварительно должен бы установлен <a href="https://www.docker.com/">Docker<a>)
<br>
## Celery task
Для запуска приложения с Celery[RabbitMQ] (с таской читающей excel и апдейтящей бд)<br>
в корневой директории в консоли выполнить: `docker-compose -f docker-compose-with-celery-task up -d`<br>
Файл `Menu.xlsx` находится в папке `admin` в контейнере с <b>Celery</b><br>
- при работе с эксель таблицей, предполагается что при добавлении новых элементов <br>
слева от них будут вписываться новые <a href="https://uuidgen.org/v/4">UUID v4<a>
- а так же предполагается что будет сохраняться правильная структура элементов
- в колонке со скидками (справа от цены) при отсутствии скидки должно быть указано `0`
- :skull_and_crossbones:осторожно, при чтении алгоритмов выполнения таски может сломаться мозг!:skull_and_crossbones:

#### Работа с докером:
- Чтобы быстро кильнуть все контейнеры советую использовать команду `docker rm -f $(docker ps -aq)`
- Чтобы поднять контейнеры с учётом изменений в файлах (без кеширования) ` docker-compose up -d --build`
