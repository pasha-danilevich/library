from faker import Faker
import random
from django.core.management.base import BaseCommand
from catalog.models import Author, Genre, Book

class Command(BaseCommand):
    help = 'Generate random data for Author, Genre and Book models'

    def add_arguments(self, parser):
        parser.add_argument('--number_of_iterations', type=int, help='Number of iterations')

    def handle(self, *args, **kwargs):
        fake = Faker()
        number_of_iterations = kwargs['number_of_iterations']

        for _ in range(number_of_iterations):
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