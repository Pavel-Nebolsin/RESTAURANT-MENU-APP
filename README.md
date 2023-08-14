# Y_LAB_MENU_APP

## Тесты
Для запуска приложения с ТЕСТАМИ (пустая база для pytest и postman) корневой директории в консоли выполнить:<br>
`docker-compose -f docker-compose-test.yml up -d`<br>
Когда все контейнеры запустятся, можно запустить тесты командой:<br>
`docker exec crud_tests pytest --color=yes -s -v /app/tests`<br>
<br>
## Celery task
Для запуска приложения с Celery[RabbitMQ] (с таской читающей excel и апдейтящей бд) в корневой директории в консоли выполнить:<br>
`docker-compose up -d`<br>
`Menu.xlsx` находится в папки admin в контейнере с Celery





(предварительно должен бы установлен <a href="https://www.docker.com/">Docker<a>)

Дополнительно:<br>

Все pre-commit хуки и линтеры проходят без ошибок.<br>
Чтобы в этом убедиться, необходимо:
- создать `виртуальное окружение` и уставновить в него все зависимости из `requirements.txt` в корневой директории реппозитория.
- далее там же инициировать `git` командой `git init`
- добавить все файлы командой `git add . `
- установить прекоммит конфиг командой `pre-commit install`
- запустить прекоммит командой `pre-commit run --all-files`
