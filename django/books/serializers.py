from rest_framework import serializers
from .models import (
    Book,
    Category,
    Thread,
    Comment,
    UserLibrary,
    Community,
    CommunityComment,
    TopBook,
)
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "profile_image"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "thread",
            "created_at",
            "likes_count",
            "is_liked",
        ]
        read_only_fields = ["id", "author", "likes_count", "is_liked"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class ThreadSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    # ✅ 읽기용 (프론트에 전체 book 정보 전달)
    book = BookSerializer(read_only=True)

    # ✅ 쓰기용 (프론트에서 book.id를 보낼 수 있도록 허용)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "content",
            "writer",
            "book",
            "book_id",
            "read_date",
            "comments",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = [
            "id",
            "writer",
            "book",
            "comments",
            "likes_count",
            "comments_count",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class UserLibrarySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = UserLibrary
        fields = ["id", "book", "added_date"]


class CommunityCommentSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)

    class Meta:
        model = CommunityComment
        fields = ["id", "content", "created_at", "updated_at", "writer", "post"]
        read_only_fields = ["id", "created_at", "updated_at", "writer"]


class CommunitySerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source="book"
    )
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_popular = serializers.SerializerMethodField()
    comments = CommunityCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = [
            "id",
            "category",
            "category_display",
            "title",
            "content",
            "created_at",
            "updated_at",
            "writer",
            "book",
            "book_id",
            "likes_count",
            "is_liked",
            "is_popular",
            "comments",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "writer"]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_is_popular(self, obj):
        return obj.is_popular

class TopBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = TopBook
        fields = ['id', 'book', 'rank']
        read_only_fields = ['id']
