from django.contrib import admin
from django.urls import path
from .views import BookListView, CategoryListView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
]