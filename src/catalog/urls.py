# catalog/urls.py

from django.urls import path
from .views import BookCatalogView

urlpatterns = [
    path('', BookCatalogView.as_view(), name='catalog'),
]