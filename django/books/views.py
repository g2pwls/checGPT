from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer
from django.db.models import Q 

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

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class BookDetailView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .utils import generate_audio_for_book
from django.shortcuts import get_object_or_404

class BookAudioGenerateView(APIView):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        try:
            generate_audio_for_book(book)
            return Response({"message": "Audio generated successfully.", "audio_file": book.audio_file.url})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def recommended_books(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        recommended = Book.objects.filter(
            Q(category=book.category) | Q(author=book.author)
        ).exclude(id=book.id).order_by('?')[:3]
        serializer = BookSerializer(recommended, many=True)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def book_detail(request, id):
    book = Book.objects.get(pk=id)
    return Response(BookSerializer(book).data)