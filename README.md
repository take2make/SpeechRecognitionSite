# SPEECH RECOGNITION SITE

Для обработки аудио речи в текст используется спроектированное api (https://github.com/take2make/sra_api.git).

## Процесс запуска и установки (unix системы)

> git clone https://github.com/take2make/sra_api.git

> cd sra_api

Создание виртуального окружения

> python3 -m venv venv

Активация виртуального окружения

> source venv/bin/activate

Установка необходимых зависимостей

> pip3 install -r requirements.txt

## Запуск

> python3 manage.py runserver

Прежде, может понадобится запустить необходимые миграции:
python3 manage.py makemigrations
python3 manage.py migrate

## Пример запущенного приложения

[!alt tag](https://github.com/take2make/sra_api/blob/main/view.png)
