# Y_LAB_MENU_APP
Для запуска всех контейнеров в корневой директории в консоли выполнить:<br>
`docker-compose up -d`<br>

Когда все контейнеры запустятся, можно запустить тесты командой:<br>
`docker exec crud_tests pytest --color=yes -s -v /app/tests/tests.py`<br>

(предварительно должен бы установлен <a href="https://www.docker.com/">Docker<a>)
