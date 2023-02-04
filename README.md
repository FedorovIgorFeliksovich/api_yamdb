# api_final
## Авторы:
Игорь Фёдоров [FedorovIgorFeliksovich] (https://github.com/FedorovIgorFeliksovich)
Александр Каваленко (amater95)
Роман Турундаев (RomanTurundaev)

## Описание:

YaMDb - это платформа для сбора отзывов и оценок по различным категориям.
(REST API для YaMDb, создан на основе библиотеки Django REST Framework (DRF))

## Технологии:
Python 3.9
Django 3.2

## Инструкция запуска проекта на локальной машине (Win):
1. Клонировать репозиторий c помощью SSH-ключа и перейти в него в командной строке:
```
git clone git@github.com:FedorovIgorFeliksovich/api_yamdb.git
```
```
cd <Путь до папки проекта>/api_yamdb
```
2. Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
3. Обновить менеджер pip
```
python -m pip install --upgrade pip
```
4. Установить зависимости из файла requirements.txt:
```
python -m pip install -r requirements.txt
```
5. Выполнить миграции:
```
python manage.py makemigrations users
python manage.py makemigrations reviews
python manage.py makemigrations api
python manage.py migrate
```
6. Выполнить загрузку информации в базу данных:
```
python manage.py import_csv
```
7. Запустить проект:
```
python manage.py runserver
```

### После запуска проекта,, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API YaMDb (в формате Redoc). В документации описана работа API. 

## Примеры запросов
1. Добавление новой категории администратом на url 'https://127.0.0.1:8000/api/v1/categories/:
Request samples:
```
{
  "name": "string",
  "slug": "string"
}
```
Response samples:
```
{
  "name": "string",
  "slug": "string"
}
```
2. Добавление новой категории на url http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/:
Request samples:
```
{
  "text": "string",
  "score": 1
}
```
Response samples:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
