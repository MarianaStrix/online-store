# Что это? 

REST API сервис интернет-магазина, который позволяет произвести анализ рынка,
для оптимизации продаж. У магазина есть поставщик, регулярно присылающий 
выгрузки данных с информацией о жителях. Проанализировав их, можно выявить 
спрос на подарки в разных городах у жителей разных возрастных групп по месяцам.

Данный сервис сохраняет переданные ему наборы данных c жителями (выгрузки от поставщика). 
Сервис позволяет их просматривать, редактировать информацию об отдельных 
жителях, производить анализ возрастов жителей по городам и 
анализировать спрос на подарки в разных месяцах для указанного набора данных.
Так же реализована возможность загрузить несколько независимых наборов
данных с разными идентификаторами, независимо друг от друга изменять
и анализировать их.


## Требования

Тестирование приложения проводилось на следующей конфигурации:
* Ubuntu 18.04.3
* Python 3.6.8
* PostgreSQL 11.5
* nginx 1.17.3
* NGINX Unit 1.10.0

## Установка

В примере будет рассмотрена машина с Ubuntu 18.04.3 (Bionic).
Для развертывания проекта на сервере, необходимо выполнить следующие действия:

1. Добавляем необходимые репозитории:
    ```shell script
    # Репозиторий nginx
    echo "deb http://nginx.org/packages/mainline/ubuntu bionic nginx" \
        | sudo tee /etc/apt/sources.list.d/nginx.list
    
    # Репозиторий NGINX Unit
    echo "deb https://packages.nginx.org/unit/ubuntu/ bionic unit" \
        | sudo tee /etc/apt/sources.list.d/unit.list
    
    # Репозиторий PostgreSQL
    echo "deb https://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" \
        | sudo tee /etc/apt/sources.list.d/pgdg.list
    ```

2. Устанавливаем ключи для репозиториев:
    ```shell script
    # Ключ Nginx
    curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo apt-key add -
    
    # Ключ Unit
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    
    # Обновляем кеш
    sudo apt-get update
    ```

3. Устанавливаем необходимые пакеты:
    ```shell script
    sudo apt-get install nginx \
                         unit \
                         unit-python3.6 \
                         postgresql-11 \
                         postgresql-server-dev-11 \
                         python3 \
                         python3-pip \
                         python3-setuptools \
                         python3-venv \
                         ca-certificates \
                         git
    ```

3. Создаем пользователя для работы сервиса:
    ```shell script
    sudo adduser --disabled-login --gecos 'Store' store
    ```   
4. Создаем виртуальное окружение и устанавливаем python-зависимости:
    ```shell script
    mkdir /srv/yandex-school
    python3 -m venv /srv/yandex-school/venv
    source /srv/yandex-school/venv/bin/activate
    cd 
    git clone git@github.com:MarianaStrix/online-store.git .
    ```
    
3. Установка и настройка PostgreSQL
4. Установка и настройка вертуальное окружение
5. Установка requirements.txt
6. Миграция базы
   ```shell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
Тестирование
------------
Для выполнения тестов необходимо:

Тесты не рекомендуется делать на продакшене, поэтому даннаю последовательность 
действий лучше выполнять на тестовых машинах.

1. Установить и настроить PostgreSQL

   1.1. Если на машине нет PostgreSQL, то необходимо установить:
   ```shell script
   $ sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
   $ curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
   $ apt update
   $ apt install postgresql-11
   ```
   > P.S. Определяет операционную систему
   >```shell script
   >$ (lsb_release -cs) 
   >```
   > P.S.S. [Ссылка на инструкцию](https://wiki.postgresql.org/wiki/Apt) 

   1.2. Создать базу, пользователя и дать права пользователю на данную базу.
   
   ```sql
   sudo -u postgres psql
   CREATE DATABASE db_store;
   CREATE USER admin WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE db_store TO admin;
   ```
   
2. Склонировать проект из Git репозитория

    ```shell script
    git clone git@github.com:MarianaStrix/online-store.git
    ```
   
3. Установить вертуальное окружение
 
   3.1. Находясь в папке проекта выполните команду:
 
   ```shell script
   python3 -m venv namevenv
   ```
   
   3.2. Войдите в окружение
   
   ```shell script
   source venv/bin/activate
   ```
4. Установка зависимостей

   В проекте имеется два файла *requirements/requirements-dev.txt* и
*requirements/requirements.txt*. Для нашего варианта необходимо установить
первый файл, с помощью команды:

   ```shell script
   pip install -r requirements/requirements-dev.txt 
   ```
5. Настроить .env
  
   В проекте для безопасности используются переменные окружения. В частности
   используется библиотека *django-environ==0.4.5*.

   5.1. В папке *onlinestore/settings* создайте файл .env, по примеру файла .env.example
   5.2. Запишите настройки в файл .env по примеру ниже
   
   ```shell
   DEBUG=False
   SECRET_KEY=you_django_secret_key
   ALLOWED_HOSTS=127.0.0.1,example.com
   DATABASE_URL=psql://user_name:password@127.0.0.1:5432/db_store
   ENVIRONMENT=production 
   ```

6. Запустить тесты

   Для тестов используется две библтотеки: *pytest*, *pytest-django*.
   
   Для тестов используются отдельные настройки, а точнее база указанная в файле *onlinestore/settings/tests.py*.
   При запуске тестов создаётся тестовая база данных, в соответствии с настройками в onlinestore/settings/tests.py. 
   Изменения в базе данных, сделанные в каждом отдельном тесте, не влияют на другие тесты, благодаря тому, что по 
   завершение каждого теста отменяется транзакция, начатая в его начале. По завершении выполнения всех тестов база 
   удаляется.
   
   Для этого сервиза разработан комплекс тестов для каждой конечной точки.
   Тестиование можно проводить двумя способами:
   
   6.1. Запуск всех тестов 
   
   ```shell script
   pytest --ds=onlinestore.settings.tests --nomigrations
   ```
   
   > --ds=yourproject.settings данный ключ указывает на настройки для тестов

   > --nomigrations данный ключ отключает миграции и создаст базу данных путем проверки 
   всех моделей, это в некоторых случаях ускоряет тестирование
   
   6.2. Запуск отдельных модулей
   
   ```shell script
   export DJANGO_SETTINGS_MODULE=onlinestore.settings.tests
   pytest tests/test_citizen_update_view.py --nomigrations
   ```
   > --nomigrations данный ключ отключает миграции и создаст базу данных путем проверки 
   всех моделей, это в некоторых случаях ускоряет тестирование
   
   Вторая страка указывает на определенный модуль, всего возможны следующие модули:
    ```shell script
   tests/test_import_create_view.py
   tests/test_import_get_view.py
   tests/test_citizen_update_view.py
   tests/test_import_birthdays_view.py
   tests/test_import_percentile_view.py
   ```
