from rest_framework import serializers
from .models import Book, Category, Thread, Comment, UserLibrary, TopBook
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'profile_image']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

class ThreadSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    # ✅ 읽기용 (프론트에 전체 book 정보 전달)
    book = BookSerializer(read_only=True)

    # ✅ 쓰기용 (프론트에서 book.id를 보낼 수 있도록 허용)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )

    class Meta:
        model = Thread
        fields = [
            'id', 'title', 'content', 'writer',
            'book', 'book_id', 'read_date',
            'comments', 'likes_count', 'comments_count',
        ]
        read_only_fields = ['id', 'writer', 'book', 'comments', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class UserLibrarySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = UserLibrary
        fields = ['id', 'book', 'added_date']

class TopBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = TopBook
        fields = ['id', 'book', 'rank']
        read_only_fields = ['id']
