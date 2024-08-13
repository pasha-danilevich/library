from rest_framework import serializers
from auth_app.models import Reader
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
        

class ReaderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reader
        fields = ['first_name', 'last_name', 'address']

class DebtorSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    reader = ReaderSerializer()
    
    class Meta:
        model = BorrowedBook
        fields = ['reader', 'book', 'borrow_date']