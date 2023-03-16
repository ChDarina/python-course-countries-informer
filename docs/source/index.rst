Справочник по странам и городам
****************

Веб-сервис для получения актуальной информации о странах и городах.
Приложение позволяет получать из открытых источников информацию о странах и городах (географические данные, валюты, погода)
и предоставлять её пользователю.

Установка
=========

Установите требуемое ПО:

1. Docker для контейнеризации – |link_docker|

.. |link_docker| raw:: html

   <a href="https://www.docker.com" target="_blank">Docker Desktop</a>

2. Для работы с системой контроля версий – |link_git|

.. |link_git| raw:: html

   <a href="https://github.com/git-guides/install-git" target="_blank">Git</a>

3. IDE для работы с исходным кодом – |link_pycharm|

.. |link_pycharm| raw:: html

    <a href="https://www.jetbrains.com/ru-ru/pycharm/download" target="_blank">PyCharm</a>

Клонируйте репозиторий проекта в свою рабочую директорию:

    .. code-block:: console

        git clone https://github.com/MNV/python-course-countries-informer.git

Использование
=============

Перед началом использования приложения необходимо его сконфигурировать.

.. note::

    Для конфигурации выполните команды, описанные ниже, находясь в корневой директории проекта.

1. Скопируйте файл настроек `.env.sample`, создав файл `.env`:
    .. code-block:: console

        cp .env.sample .env

    Этот файл содержит преднастроенные переменные окружения, значения которых будут общими для всего приложения.
    Файл примера (`.env.sample`) содержит набор переменных со значениями по умолчанию.
    Созданный файл `.env` можно настроить в зависимости от окружения.

    .. warning::

        Никогда не добавляйте в систему контроля версий заполненный файл `.env` для предотвращения компрометации информации о конфигурации приложения.

    Чтобы получить доступ к API внешних систем, посетите соответствующие сервисы и получите токены доступа:

    * APILayer — Geography API (https://apilayer.com/marketplace/geo-api)
    * OpenWeather – Weather Free Plan (https://openweathermap.org/price#weather)
    * NewsAPI — News API (https://newsapi.org/register)

    Задайте полученные токены доступа в качестве значений переменных окружения (в файле `.env`):

    * `API_KEY_APILAYER` – для токена доступа к APILayer
    * `API_KEY_OPENWEATHER` – для токена доступа к OpenWeather
    * `API_KEY_NEWSAPI` - для токена доступа к NewsAPI

2. Соберите Docker-контейнер с помощью Docker Compose:
    .. code-block:: console

        docker compose build

    Данную команду необходимо выполнять повторно в случае обновления зависимостей в файле `requirements.txt`.

3. Чтобы просмотреть документацию по использованию консольного приложения, выполните:
    .. code-block:: console

        docker compose run app python main.py --help

    Данная команда выведет на экран список доступных аргументов и их значения по умолчанию.

4. Для запуска приложения выполните:
    .. code-block:: console

        docker compose up

    Когда контейнеры запустятся, приложение можно будет открыть по адресу: http://0.0.0.0:8020 в браузере.
5. Собираемые в приложении данные кэшируются для оптимизации частоты запросов.
   Частота обновления данных зависит от настроек в переменных:
    * `CACHE_TTL_CURRENCY_RATES` (время актуальности данных о курсах валют)
    * `CACHE_TTL_WEATHER` (время актуальности данных о погоде)

    Значение для этих переменных указывается в секундах (они определяются в файле `.env`).

Автоматизация
=============

Проект содержит специальный файл (`Makefile`) для автоматизации выполнения команд:

1. Сборка Docker-контейнера.
2. Генерация документации.
3. Запуск форматирования кода.
4. Запуск статического анализа кода (выявление ошибок типов и форматирования кода).
5. Запуск автоматических тестов.
6. Запуск всех функций поддержки качества кода (форматирование, линтеры, автотесты).

Инструкция по запуску этих команд находится в файле `README.md`.

Тестирование
============

Для запуска автоматических тестов выполните команду:

.. code-block:: console

    docker compose run app pytest --cov=/src --cov-report html:htmlcov --cov-report term --cov-config=/src/tests/.coveragerc -vv

Также существует аналогичная `make`-команда:

.. code-block:: console

    make test

Отчет о тестировании находится в файле `src/htmlcov/index.html`.

Документация к исходному коду
*****************************

.. toctree::
   :maxdepth: 2
   :caption: Содержимое:

.. index:: view, base

Сервис по сбору географических данных
===========
.. toctree::
   :maxdepth: 2
   :caption: Содержимое:

Клиенты
-------
Страны и города
^^^^^^^^^^^^^^^
.. automodule:: geo.clients.geo
   :members:

Валюты и их курсы
^^^^^^
.. automodule:: geo.clients.currency
   :members:

Погода
^^^^^^
.. automodule:: geo.clients.weather
   :members:

Схемы
^^^^^
.. automodule:: geo.clients.shemas
   :members:

Сервисы
-------
Страна
^^^^^^^^^^^^^^^
.. automodule:: geo.services.country
   :members:

Город
^^^^^^^^^^^^^^^
.. automodule:: geo.services.city
   :members:

Валюта
^^^^^^
.. automodule:: geo.services.currency
   :members:

Погода
^^^^^^
.. automodule:: geo.services.weather
   :members:

Схемы
^^^^^
.. automodule:: geo.services.shemas
   :members:

Отображения
------
.. automodule:: geo.views
   :members:

.. index:: view, base

Сервис сбора новостей
============
.. toctree::
   :maxdepth: 2
   :caption: Содержимое:

Клиенты
-------
.. automodule:: news.clients.news
   :members:

Сервисы
-------
.. automodule:: news.services.news
   :members:

Views
------
.. automodule:: news.views
   :members: