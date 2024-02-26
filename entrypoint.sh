#!/bin/sh

# Подготовка и установка SSL-сертификата с помощью Certbot
certbot certonly --nginx --non-interactive --agree-tos --email mfalcon@mail.ru -d obs-balashiha.ru -d www.obs-balashiha.ru

# Перезапуск Nginx для применения изменений
service nginx restart

# Выполнение миграций и других необходимых команд
python manage.py migrate --run-syncdb
python manage.py loaddata dbdump.json
#python manage.py collectstatic --no-input
gunicorn belogo_new.wsgi:application --bind 0.0.0.0:8080 --reload -w 4
