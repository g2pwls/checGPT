from django.contrib import admin
from django.urls import path
from .views import BookListView, CategoryListView, BookDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', BookListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('api/books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
]