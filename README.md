# Y_LAB_MENU_APP
Для запуска всех контейнеров в корневой директории в консоли выполнить:<br>
`docker-compose up -d --build`<br>

Когда все контейнеры запустятся, можно запустить контейнер с тестами командой:<br>
`docker-compose run --rm tests pytest -s -v /app/tests/tests.py`<br>

(предварительно должен бы установлен <a href="https://www.docker.com/">Docker<a>)
