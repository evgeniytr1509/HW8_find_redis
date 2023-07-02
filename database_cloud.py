import json
from mongoengine import *

# Установка подключения к MongoDB
connect('database_cloud', host='mongodb+srv://userweb12:!123456!@cluster1.adkti2c.mongodb.net/')

# Модель для авторов
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Модель для цитат
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

# Загрузка данных авторов из JSON-файла и сохранение в коллекции "authors"
with open('authors.json') as f:
    authors_data = json.load(f)

for author_data in authors_data:
    author = Author(
        fullname=author_data['fullname'],
        born_date=author_data['born_date'],
        born_location=author_data['born_location'],
        description=author_data['description']
    )
    author.save()

# Загрузка данных цитат из JSON-файла и сохранение в коллекции "quotes"
with open('quotes.json') as f:
    quotes_data = json.load(f)

for quote_data in quotes_data:
    #author = Author.objects.get(fullname=quote_data['author'])
    #author = Author.objects(firstname=quote_data['author']).first()
    author = Author.objects(fullname=quote_data['author']).first()
    quote = Quote(
        tags=quote_data['tags'],
        author=author,
        quote=quote_data['quote']
    )
    quote.save()
