from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookListView,
    CategoryListView,
    BookDetailView,
    BookAudioGenerateView,
    ThreadListCreateView,
    ThreadDetailView,
    thread_like,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    add_to_library,
    remove_from_library,
    UserLibraryView,
    UserThreadsView,
    comment_like,
    toggle_book_like,
    CommunityListCreateView,
    CommunityDetailView,
    toggle_community_like,
    create_community_comment,
    delete_community_comment,
    TopBooksView,
    BookViewSet,
    AIReportViewSet,
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'ai-reports', AIReportViewSet, basename='ai-report')

urlpatterns = [
    path('', include(router.urls)),
    path("books/", BookListView.as_view()),
    path("categories/", CategoryListView.as_view()),
    path("books/<int:book_id>/", BookDetailView.as_view(), name="book_detail"),
    path("books/<int:book_id>/generate-audio/", BookAudioGenerateView.as_view()),
    path("books/<int:book_id>/like/", toggle_book_like, name="book-like"),
    path(
        "books/<int:book_id>/threads/",
        ThreadListCreateView.as_view(),
        name="book-threads",
    ),
    path("threads/", ThreadListCreateView.as_view(), name="thread-list-create"),
    path("threads/<int:pk>/", ThreadDetailView.as_view()),
    path("threads/<int:pk>/like/", thread_like),
    path("comments/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/", CommentUpdateView.as_view(), name="comment-update"),
    path(
        "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
    path("comments/<int:pk>/like/", comment_like),
    # Library endpoints
    path("books/<int:book_id>/add-to-library/", add_to_library),
    path("books/<int:book_id>/remove-from-library/", remove_from_library),
    path("users/library/", UserLibraryView.as_view()),
    path("users/<int:user_id>/library/", UserLibraryView.as_view()),
    # User threads endpoint
    path('users/<int:user_id>/threads/', UserThreadsView.as_view()),
    path('users/top-books/', TopBooksView.as_view(), name='user-top-books'),
    path('users/<int:user_id>/top-books/', TopBooksView.as_view(), name='user-top-books-detail'),
    path("users/<int:user_id>/threads/", UserThreadsView.as_view()),
    path(
        "books/<int:book_id>/community/",
        CommunityListCreateView.as_view(),
        name="community-list",
    ),
    path("community/<int:pk>/", CommunityDetailView.as_view(), name="community-detail"),
    path(
        "community/<int:pk>/like/", toggle_community_like, name="community-like"
    ),
    path(
        "community/<int:community_id>/comments/",
        create_community_comment,
        name="create_community_comment",
    ),
    path(
        "community/comments/<int:comment_id>/",
        delete_community_comment,
        name="delete_community_comment",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
