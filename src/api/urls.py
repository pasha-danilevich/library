from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('books/', include('api.book.urls'))
]
