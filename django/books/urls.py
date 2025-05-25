from django.contrib import admin
from django.urls import path
from .views import BookListView, CategoryListView, BookDetailView, BookAudioGenerateView, ThreadListCreateView, ThreadDetailView, thread_like
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('books/', BookListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:book_id>/generate-audio/', BookAudioGenerateView.as_view()),
    path('books/<int:book_id>/recommendations/', views.recommended_books),
    path('books/<int:book_id>/threads/', ThreadListCreateView.as_view(), name='book-threads'),
    path('threads/', ThreadListCreateView.as_view(), name='thread-list-create'),
    path('threads/<int:pk>/', ThreadDetailView.as_view()),
    path('threads/<int:pk>/like/', thread_like),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)