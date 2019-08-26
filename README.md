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
* Ubuntu 18.04.3 (все инструкции приведенные ниже указаны для этой ОС)
* Python 3.6.8
* Django 2.2.4
* Django REST framework 3.10.2
* PostgreSQL 11.5
* nginx 1.17.3
* NGINX Unit 1.10.0

## Установка

### Production окружение

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
    # Ключ nginx и NGINX Unit
    curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo apt-key add -
    
    # Ключ PostgeSQL
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
                         python3-dev \
                         gcc \
                         apt-transport-https \
                         ca-certificates \
                         git
    ```
4. Настраиваем установленные пакеты:
    ```shell script
    # Включаем автозагрузку NGINX Unit
    sudo systemctl enable unit
   
    # Удаляем стандартные конфиграционные файлы nginx
    sudo rm -f /etc/nginx/nginx.conf
    sudo rm -f /etc/nginx/default.conf
   
    # Создаем конфигурационный файл NGINX Unit (под root)
    cat << EOF > /etc/unit/config.json
    {
         "settings": {
             "http": {
                 "max_body_size": 52428800
             }
         },
    
        "listeners": {
            "127.0.0.1:8081": {
                "pass": "applications/yandex-school"
            }
        },
    
        "applications": {
            "yandex-school": {
                "type": "python",
                "processes": 4,
                "path": "/srv/yandex-school/online-store/",
                "home": "/srv/yandex-school/venv/",
                "module": "onlinestore.wsgi",
                "user": "store",
                "group": "store"
            }
        }
    }
    EOF
    
    # Создаем конфигурационный файл nginx (под root)
    cat << EOF > /etc/nginx/nginx.conf
    
    user nginx;
    worker_processes auto;
    worker_rlimit_nofile 65536;
    
    pid /var/run/nginx.pid;
    
    events {
        worker_connections 8192;
    }
    
    
    http {
        include /etc/nginx/mime.types;
        default_type application/octet-stream;
    
        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';
    
        server_tokens off;
    
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
    
        keepalive_timeout 65;
    
        gzip on;
        gzip_disable "msie6";
        gzip_vary on;
        gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
        gzip_proxied any;
    
        include /etc/nginx/conf.d/*.conf;
    }
    EOF
   
    # Создаем конфигураационный файл сайта (под root)
    cat << EOF > /etc/nginx/conf.d/yandex-school.conf
    upstream unit_backend_api {
        server 127.0.0.1:8081;
    }
    
    server {
        listen 80;
        listen 8080;
        server_name yandex-school.marianastrix.com;
    
        access_log /var/log/nginx/yandex-school.access.log main;
        error_log /var/log/nginx/yandex-school.error.log warn;
    
        client_max_body_size 50M;
    
        location / {
            proxy_pass http://unit_backend_api;
            proxy_set_header Host $host;
        }
    
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
    EOF
   
    # Увеличиваем лимиты системы (под root)
    echo "net.ipv4.tcp_max_syn_backlog = 4096" >> /etc/sysctl.conf
    echo "net.core.somaxconn = 4096" >> /etc/sysctl.conf
   
    mkdir -p /etc/systemd/system/unit.service.d/
    mkdir -p /etc/systemd/system/nginx.service.d/

    cat << EOF > /etc/systemd/system/nginx.service.d/nginx.conf
    [Service]
    LimitNOFILE=32768
    EOF

    cat << EOF > /etc/systemd/system/unit.service.d/unit.conf
    [Service]
    LimitNOFILE=32768
    EOF
   
    # Применяем изменения для systemd-unit файлов
    sudo systemctl daemon-reload
   
    # Применяем конфигурацию NGINX Unit
    sudo curl -X PUT -d @/etc/unit/config.json --unix-socket /run/control.unit.sock http://localhost/config
   
    # Применяем конфигурацию nginx
    sudo systemctl restart nginx
    ```

8. Создаем пользователя и базу в PostgreSQL:
    ```shell script
    sudo -u postgres psql
    
    # Выполняем запросы в консоли СУБД
    CREATE DATABASE db_onlinestore;
    CREATE USER store WITH PASSWORD '<ваш_пароль>';
    GRANT ALL PRIVILEGES ON DATABASE db_onlinestore TO store;
    ```

5. Создаем пользователя для работы сервиса и даем ему права на директорию сервиса:
    ```shell script
    sudo adduser --disabled-login --gecos 'Store' store
    sudo mkdir /srv/yandex-school
    sudo chown store. /srv/yandex-school
    ```
   
6. Генерируем ssh-ключ для пользователя:
    ```shell script
    sudo -i -u store
    ssh-keygen -t rsa -b 4096
   
    # Выводим ключ
    cat /home/store/.ssh/id_rsa
    ```
7. Добавляем ключ в репозиторий на GitHub в соответствии с [официальной инструкцией](https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys)

9. Создаем виртуальное окружение:
    ```shell script
    python3 -m venv /srv/yandex-school/venv
    source /srv/yandex-school/venv/bin/activate
    ```

10. Клонируем код проекта:
    ```shell script
    cd /srv/yandex-school
    git clone git@github.com:MarianaStrix/online-store.git
    ```
11. Установка python-зависимостей проекта:
    ```shell script
    cd ./online-store
    pip3 install -r ./requirements/requirements.txt
    ```

12. Применяем миграции базы:
    ```shell script
    python3 manage.py migrate
    ```

13. Создаем административного пользователя:
    ```shell script
    python3 manage.py createsuperuser
    ```

14. Настраиваем сервис:
    ```shell script
    cp ./onlinestore/settings/.env.example ./onlinestore/settings/.env
    nano ./onlinestore/settings/.env
    
    # Настраиваем параметры
    DEBUG=False
    SECRET_KEY=<случайно_сгенерированный_ключ_длинной_50_символов>
    ALLOWED_HOSTS=127.0.0.1,yandex-school.marianastrix.com
    DATABASE_URL=psql://store:<ваш_пароль>@127.0.0.1:5432/db_onlinestore
    ENVIRONMENT=production
    ```

15. Запускаем сервер
    ```shell script
    sudo systemctl restart unit
    ```

### Development окружение

Для развертывания проекта в режиме разработки, необходимо выполнить следующие действия:

1. Добавляем репозиторий PostgreSQL:
    ```shell script
    echo "deb https://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" \
        | sudo tee /etc/apt/sources.list.d/pgdg.list
    ```

2. Устанавливаем ключи для репозитория PostgreSQL:
    ```shell script
    # Ключ PostgreSQL
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    
    # Обновляем кеш
    sudo apt-get update
    ```

3. Устанавливаем необходимые пакеты:
    ```shell script
    sudo apt-get install postgresql-11 \
                         postgresql-server-dev-11 \
                         python3 \
                         python3-pip \
                         python3-setuptools \
                         python3-venv \
                         python3-dev \
                         gcc \
                         apt-transport-https \
                         ca-certificates \
                         git
    ```
4. Создаем пользователя и базу в PostgreSQL:
    ```shell script
    sudo -u postgres psql
   
    # Выполняем запросы в консоли СУБД
    CREATE DATABASE db_onlinestore;
    CREATE USER store WITH PASSWORD '<ваш_пароль>';
    GRANT ALL PRIVILEGES ON DATABASE db_onlinestore TO store;
    ```
   
5. Генерируем ssh-ключ для себя:
    ```shell script
    ssh-keygen -t rsa -b 4096
   
    # Выводим ключ
    cat ~/.ssh/id_rsa
    ```
6. Добавляем ключ в репозиторий на GitHub в соответствии с [официальной инструкцией](https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys)

7. Создаем виртуальное окружение:
    ```shell script
    mkdir ~/yandex-school
    python3 -m venv ~/yandex-school/venv
    source ~/yandex-school/venv/bin/activate
    ```

7. Клонируем код проекта:
    ```shell script
    cd ~/yandex-school
    git clone git@github.com:MarianaStrix/online-store.git
    ```

8. Установка python-зависимостей проекта:
    ```shell script
    cd ./online-store
    pip3 install -r ./requirements/requirements-dev.txt
    ```

9. Применяем миграции базы:
    ```shell script
    python3 manage.py migrate
    ```

10. Создаем административного пользователя:
    ```shell script
    python3 manage.py createsuperuser
    ```
11. Настраиваем сервис:
    ```shell script
    cp ./onlinestore/settings/.env.example ./onlinestore/settings/.env
    nano ./onlinestore/settings/.env
    
    # Настраиваем параметры
    DEBUG=False
    SECRET_KEY=<случайно_сгенерированный_ключ_длинной_50_символов>
    ALLOWED_HOSTS=127.0.0.1,localhost
    DATABASE_URL=psql://store:<ваш_пароль>@127.0.0.1:5432/db_onlinestore
    ENVIRONMENT=development
    ```

12. Запускаем сервер:
    ```shell script
    python3 manage.py runserver
    ```

## Тестирование

Для тестов используется две библиотеки: *pytest* и *pytest-django*. 
Тестирование проводится в development окружении.

Тесты используют отдельные настройки, а, точнее, база указанная в файле *onlinestore/settings/tests.py*.
Данные тесты очищают базу данных между тестами, чтобы изолировать их и не засорять 
основную development базу.

Для этого сервиса разработан комплекс тестов для каждой конечной точки.
Тестирование можно проводить двумя способами (необходимо зайти в виртульное окружение virtualenv):
   
1. Запуск всех тестов для всех модулей
   
    ```shell script
    pytest --ds=onlinestore.settings.tests --nomigrations
    ```
   
    > --ds=yourproject.settings данный ключ указывает на настройки для тестов

    > --nomigrations данный ключ отключает миграции и создаст базу данных путем проверки 
    всех моделей, это в некоторых случаях ускоряет тестирование
   
2. Запуск тестов для отдельных модулей
   
    ```shell script
    export DJANGO_SETTINGS_MODULE=onlinestore.settings.tests
    pytest tests/test_citizen_update_view.py --nomigrations
    ```
    > --nomigrations данный ключ отключает миграции и создаст базу данных путем проверки 
    всех моделей, это в некоторых случаях ускоряет тестирование
   
    Вторая строка указывает на определенный модуль, всего возможны следующие модули:
    ```shell script
    tests/test_import_create_view.py
    tests/test_import_get_view.py
    tests/test_citizen_update_view.py
    tests/test_import_birthdays_view.py
    tests/test_import_percentile_view.py
    ```

## Комментарии к проекту

1. Применение, для вычисления возраста на уровне базы данных, функция PostgreSQL age(), 
предполагает, что эксплуатироваться приложение будет совместно именно с этой СУБД.
Однако переход на другую СУБД, при необходимости потребует лишь небольшого изменения RawSQL-запроса.

2. Сервис доступен как напрямую по IP-адресу http://84.201.155.85:8080 так и по адресу http://yandex-school.marianastrix.com:8080
Так же сервис доступен по 80 и 443 порту c использованием TLS 1.2: https://yandex-school.marianastrix.com
