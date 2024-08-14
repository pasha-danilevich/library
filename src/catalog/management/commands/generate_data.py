from faker import Faker
import random
from django.core.management.base import BaseCommand
from catalog.models import Author, Genre, Book

class Command(BaseCommand):
    help = 'Generate random data for Author, Genre and Book models'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(10):
            # Создание случайных авторов
            author = Author.objects.create(name=fake.name())
            
            # Создание случайных жанров
            genre = Genre.objects.create(name=fake.word())
            
            # Создание случайных книг
            book = Book.objects.create(
                title=fake.sentence(nb_words=4),
                author=author,
                genre=genre
            )
            
            self.stdout.write(f'Created book: {book.title}')