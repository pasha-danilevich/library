from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from catalog.models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

class BookList(ListModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)