import json
from mongoengine import connect, disconnect
from models import Author, Quote

# Отключение текущего подключения
disconnect(alias='default')

# Установка подключения к облачной базе данных MongoDB
connect('database_cloud', host='mongodb+srv://userweb12:!123456!@cluster1.adkti2c.mongodb.net/', alias='default')

# Путь к JSON-файлу с данными авторов
authors_json_file = 'authors.json'

# Загрузка данных авторов из JSON-файла и сохранение в коллекции "authors"
with open(authors_json_file) as f:
    authors_data = json.load(f)

for author_data in authors_data:
    author = Author(**author_data)
    author.save()

# Путь к JSON-файлу с данными цитат
quotes_json_file = 'quotes.json'

# Загрузка данных цитат из JSON-файла и сохранение в коллекции "quotes"
with open(quotes_json_file) as f:
    quotes_data = json.load(f)

for quote_data in quotes_data:
    authors = Author.objects.filter(fullname=quote_data['author'])
    if authors:
        author = authors[0]  # Выбираем первого автора из списка
        quote_data.pop('author')  # Удаляем ключевой аргумент 'author' из quote_data
        quote = Quote(**quote_data)
        quote.author = author  # Устанавливаем значение автора отдельно
        quote.save()
    else:
        print(f"Автор с именем '{quote_data['author']}' не найден.")

# Закрытие подключения к базе данных
disconnect(alias='default')
