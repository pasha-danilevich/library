from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from auth_app.utils import get_access_token, get_user_from_token
from catalog.models import Book, BorrowedBook
from .serializers import BookSerializer, BorrowedBookSerializer
from rest_framework.permissions import IsAuthenticated

class BookList(ListModelMixin, GenericAPIView):

    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MyBookList(ListModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    
    def get_queryset(self):
        user = self.request.user

        if user:
            queryset = self.queryset.filter(reader=user.id)
            return queryset
        return []

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)