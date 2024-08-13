from django.contrib import admin
from .models import Book, BorrowedBook, Author, Genre


admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(Author)
admin.site.register(Genre)