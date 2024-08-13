from rest_framework import serializers
from catalog.models import Author, BorrowedBook, Genre, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name')
    genre = serializers.CharField(source='genre.name')    

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre']
        
        
class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    
    class Meta:
        model = BorrowedBook
        fields = ['book', 'borrow_date']