# Y_LAB_MENU_APP
Для запуска всех контейнеров в корневой директории в консоли выполнить:
`docker-compose up -d --build`
Когда все контейнеры запустятся, можно запустить контейнер с тестами командой:
`docker-compose run --rm tests pytest -s -v /app/tests/tests.py`
