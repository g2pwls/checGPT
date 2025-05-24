from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Book, Category, Thread
from .serializers import BookSerializer, CategorySerializer, ThreadSerializer

# ----------------------
# 📚 Book 관련 API
# ----------------------

class BookListView(APIView):
    def get(self, request):
        category_id = request.query_params.get('category')
        search = request.query_params.get('search', '')
        books = Book.objects.all()

        if category_id:
            books = books.filter(category_id=category_id)
        if search:
            books = books.filter(Q(title__icontains=search) | Q(description__icontains=search))

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return Response(BookSerializer(book).data)

@api_view(['GET'])
def recommended_books(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    recommended = Book.objects.filter(
        Q(category=book.category) | Q(author=book.author)
    ).exclude(id=book.id).order_by('?')[:3]
    serializer = BookSerializer(recommended, many=True)
    return Response(serializer.data)

class BookAudioGenerateView(APIView):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        try:
            generate_audio_for_book(book)
            return Response({"message": "Audio generated successfully.", "audio_file": book.audio_file.url})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# ----------------------
# 💬 Thread 관련 API
# ----------------------

class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all().order_by('-id')
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        return get_object_or_404(Thread, id=self.kwargs['pk'])

# 좋아요 기능 (추가 예시)
@api_view(['POST'])
def thread_like(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user

    if thread.likes.filter(id=user.id).exists():
        thread.likes.remove(user)
        liked = False
    else:
        thread.likes.add(user)
        liked = True

    return Response({'liked': liked, 'likes_count': thread.likes.count()})


# views.py

@api_view(['GET'])
def user_threads(request, user_id):
    threads = Thread.objects.filter(writer__id=user_id).order_by('-id')
    serializer = ThreadSerializer(threads, many=True)
    return Response(serializer.data)
