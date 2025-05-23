from django.contrib import admin
from django.urls import path
from .views import BookListView, CategoryListView, BookDetailView, BookAudioGenerateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('books/', BookListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:book_id>/generate-audio/', BookAudioGenerateView.as_view()),
    path('books/<int:book_id>/recommendations/', views.recommended_books),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)