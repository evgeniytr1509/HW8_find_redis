from mongoengine import *
import redis

# Установка подключения к MongoDB
connect('database_cloud', host='mongodb+srv://userweb12:!123456!@cluster1.adkti2c.mongodb.net/', alias='default')

# Подключение к Redis
redis_client = redis.Redis(host='mongodb+srv://userweb12:!123456!@cluster1.adkti2c.mongodb.net/', port=6379)

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

# Функция для поиска цитат с кешированием
def search_quotes(query):
    if query.startswith('name:'):
        # Поиск цитат по имени автора с использованием кеша
        name = query.split(':', 1)[1].strip()
        cache_key = f'name:{name}'
        cached_result = redis_client.get(cache_key)
        if cached_result:
            print(cached_result.decode())
        else:
            author = Author.objects(fullname__icontains=name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    result = f'Author: {author.fullname}\nQuote: {quote.quote}\n---\n'
                    print(result)
                    redis_client.set(cache_key, result)
            else:
                print('Author not found.')
    elif query.startswith('tag:'):
        # Поиск цитат по тегу с использованием кеша
        tag = query.split(':', 1)[1].strip()
        cache_key = f'tag:{tag}'
        cached_result = redis_client.get(cache_key)
        if cached_result:
            print(cached_result.decode())
        else:
            quotes = Quote.objects(tags__icontains=tag)
            for quote in quotes:
                author = quote.author
                result = f'Author: {author.fullname}\nQuote: {quote.quote}\n---\n'
                print(result)
                redis_client.set(cache_key, result)
    elif query == 'exit':
        # Завершение выполнения скрипта
        print('Exiting the script...')
        return False
    else:
        print('Invalid command. Please try again.')

    return True

# Бесконечный цикл для выполнения команд
while True:
    command = input('Enter a command (name:<value>, tag:<value>, exit): ')
    result = search_quotes(command)
    if not result:
        break
