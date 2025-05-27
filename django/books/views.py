from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import (
    Book,
    Category,
    Thread,
    UserLibrary,
    Comment,
    Community,
    CommunityComment,
    TopBook,
    AIReport,
)
from .serializers import (
    BookSerializer,
    CategorySerializer,
    ThreadSerializer,
    UserLibrarySerializer,
    CommentSerializer,
    CommunitySerializer,
    CommunityCommentSerializer,
    TopBookSerializer,
    AIReportSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.exceptions import (
    PermissionDenied,
    NotFound,
    ValidationError,
    APIException,
)
from .utils import generate_audio_for_book
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import viewsets

# ----------------------
# 📚 Book 관련 API
# ----------------------


class BookListView(APIView):
    def get(self, request):
        category_id = request.query_params.get("category")
        search = request.query_params.get("search", "")
        books = Book.objects.all()

        if category_id:
            books = books.filter(category_id=category_id)
        if search:
            books = books.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        serializer = BookSerializer(books, many=True, context={"request": request})
        return Response(serializer.data)


class BookDetailView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book, context={"request": request})
        return Response(serializer.data)


class BookAudioGenerateView(APIView):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        try:
            generate_audio_for_book(book)
            return Response(
                {
                    "message": "Audio generated successfully.",
                    "audio_file": book.audio_file.url,
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# ----------------------
# 💬 Thread 관련 API
# ----------------------


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기 권한은 스레드 작성자에게만 허용
        return obj.writer == request.user


class ThreadListCreateView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        sort_by = self.request.query_params.get("sort_by", "latest")  # 기본값은 최신순

        if book_id:
            queryset = Thread.objects.filter(book_id=book_id)
        else:
            queryset = Thread.objects.all()

        # 정렬 적용
        if sort_by == "likes":
            # 좋아요 수로 정렬
            return queryset.annotate(likes_count=Count("likes")).order_by(
                "-likes_count"
            )
        elif sort_by == "comments":
            # 댓글 수로 정렬
            return queryset.annotate(comments_count=Count("comments")).order_by(
                "-comments_count"
            )
        else:  # 'latest'
            # 최신순 정렬 (ID 기준)
            return queryset.order_by("-id")

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        return get_object_or_404(Thread, id=self.kwargs["pk"])


# 좋아요 기능 (추가 예시)
@api_view(["POST"])
def thread_like(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user

    if thread.likes.filter(id=user.id).exists():
        thread.likes.remove(user)
        liked = False
    else:
        thread.likes.add(user)
        liked = True

    return Response({"liked": liked, "likes_count": thread.likes.count()})


# views.py
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        if comment.author != self.request.user:
            raise PermissionDenied("You can only edit your own comments.")
        return comment


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
        if comment.author != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        return comment


@api_view(["POST"])
def add_to_library(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    library_item, created = UserLibrary.objects.get_or_create(user=user, book=book)

    if not created:
        return Response(
            {"message": "이미 서재에 추가되어 있습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"message": "서재에 추가되었습니다."}, status=status.HTTP_201_CREATED
    )


@api_view(["DELETE"])
def remove_from_library(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    try:
        library_item = UserLibrary.objects.get(user=user, book=book)
        library_item.delete()
        return Response({"message": "서재에서 제거되었습니다."})
    except UserLibrary.DoesNotExist:
        return Response(
            {"message": "서재에 없는 책입니다."}, status=status.HTTP_404_NOT_FOUND
        )


class UserLibraryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None):
        try:
            # Log the incoming request details
            print(f"Request user: {request.user.id}")
            print(f"Target user_id: {user_id}")

            # Determine which user's library to fetch
            target_user_id = user_id if user_id else request.user.id
            print(f"Using target_user_id: {target_user_id}")

            # Check if the user exists
            User = get_user_model()
            if not User.objects.filter(id=target_user_id).exists():
                return Response(
                    {"error": f"User with id {target_user_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Get library items
            library_items = (
                UserLibrary.objects.filter(user_id=target_user_id)
                .select_related("book", "book__category")
                .order_by("-added_date")
            )
            print(f"Found {library_items.count()} library items")

            # Calculate top 3 genres
            genre_counts = {}
            for item in library_items:
                category = item.book.category
                if category:
                    genre_counts[category.id] = {
                        "id": category.id,
                        "name": category.name,
                        "count": genre_counts.get(category.id, {}).get("count", 0) + 1,
                    }

            # Sort genres by count and get top 3
            top_genres = sorted(
                genre_counts.values(), key=lambda x: x["count"], reverse=True
            )[:3]

            serializer = UserLibrarySerializer(library_items, many=True)
            return Response({"library": serializer.data, "top_genres": top_genres})

        except Exception as e:
            print(f"Error in UserLibraryView: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserThreadsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None):
        try:
            # Log the incoming request details
            print(f"Request user: {request.user.id}")
            print(f"Target user_id: {user_id}")

            # Determine which user's threads to fetch
            target_user_id = user_id if user_id else request.user.id
            print(f"Using target_user_id: {target_user_id}")

            # Check if the user exists
            User = get_user_model()
            if not User.objects.filter(id=target_user_id).exists():
                return Response(
                    {"error": f"User with id {target_user_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Get threads - ordering by id instead of created_at since that's the field we have
            threads = (
                Thread.objects.filter(writer_id=target_user_id)
                .select_related("book", "writer")
                .order_by("-id")
            )
            print(f"Found {threads.count()} threads")

            serializer = ThreadSerializer(threads, many=True)
            return Response(serializer.data)

        except Exception as e:
            print(f"Error in UserThreadsView: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if comment.likes.filter(id=user.id).exists():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    serializer = CommentSerializer(comment, context={"request": request})
    return Response({"is_liked": liked, "likes_count": comment.likes.count()})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_book_like(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if book.likes.filter(id=user.id).exists():
        book.likes.remove(user)
        liked = False
    else:
        book.likes.add(user)
        liked = True

    return Response({"liked": liked, "likes_count": book.likes.count()})


class CommunityListCreateView(generics.ListCreateAPIView):
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        category = self.request.query_params.get("category", "")
        queryset = Community.objects.filter(book_id=book_id)

        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        try:
            book = get_object_or_404(Book, id=self.kwargs.get("book_id"))
            if book.likes.count() < 2:
                raise PermissionDenied(
                    "이 책은 아직 커뮤니티가 활성화되지 않았습니다. (좋아요 2개 이상 필요)"
                )

            serializer.save(writer=self.request.user, book=book)
        except Book.DoesNotExist:
            raise NotFound("해당 책을 찾을 수 없습니다.")
        except PermissionDenied as e:
            raise e
        except Exception as e:
            print(f"Error in perform_create: {str(e)}")
            raise


class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if self.request.method == "GET":
            obj.views += 1
            obj.save()
        return obj


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_community_like(request, pk):
    post = get_object_or_404(Community, pk=pk)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    # save() 메서드 호출하여 is_popular 상태 업데이트
    post.save()

    return Response(
        {
            "liked": liked,
            "likes_count": post.likes.count(),
            "is_popular": post.is_popular,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_community_comment(request, community_id):
    try:
        post = Community.objects.get(pk=community_id)
    except Community.DoesNotExist:
        return Response({"error": "게시글을 찾을 수 없습니다."}, status=404)

    serializer = CommunityCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(writer=request.user, post=post)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_community_comment(request, comment_id):
    try:
        comment = CommunityComment.objects.get(pk=comment_id)
    except CommunityComment.DoesNotExist:
        return Response({"error": "댓글을 찾을 수 없습니다."}, status=404)

    if comment.writer != request.user:
        return Response({"error": "권한이 없습니다."}, status=403)

    comment.delete()
    return Response(status=204)


class TopBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        """Get user's top books"""
        try:
            # Determine which user's top books to fetch
            target_user_id = user_id if user_id else request.user.id

            # Check if the user exists
            User = get_user_model()
            if not User.objects.filter(id=target_user_id).exists():
                return Response(
                    {"error": f"User with id {target_user_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Get top books
            top_books = (
                TopBook.objects.filter(user_id=target_user_id)
                .select_related("book")
                .order_by("rank")
            )
            serializer = TopBookSerializer(top_books, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Update user's top books"""
        try:
            # Get the user's library books
            user_library = UserLibrary.objects.filter(user=request.user).values_list(
                "book_id", flat=True
            )

            # Delete existing top books
            TopBook.objects.filter(user=request.user).delete()

            # Create new top books
            top_books_data = request.data.get("top_books", [])
            created_books = []

            for rank, book_id in enumerate(top_books_data, 1):
                # Check if the book is in the user's library
                if book_id not in user_library:
                    return Response(
                        {"error": f"Book with id {book_id} is not in your library"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    book = Book.objects.get(id=book_id)
                    top_book = TopBook.objects.create(
                        user=request.user, book=book, rank=rank
                    )
                    created_books.append(top_book)
                except Book.DoesNotExist:
                    return Response(
                        {"error": f"Book with id {book_id} does not exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            serializer = TopBookSerializer(created_books, many=True)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()
        # 각 책의 댓글 수 계산
        for book in queryset:
            book.comment_count = book.community_posts.count()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 단일 책 조회 시에도 댓글 수 계산
        instance.comment_count = instance.community_posts.count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def toggle_community(self, request, pk=None):
        book = self.get_object()
        if not book.has_community:
            book.has_community = True
            book.community_created_at = timezone.now()
            book.save()
            return Response({"status": "community activated"})
        else:
            book.has_community = False
            book.community_created_at = None
            book.save()
            return Response({"status": "community deactivated"})

    @action(detail=True, methods=["post"])
    def update_stats(self, request, pk=None):
        book = self.get_object()
        # 댓글 수 업데이트
        comment_count = book.community_posts.count()
        book.comment_count = comment_count
        book.save()
        return Response(
            {"comment_count": comment_count, "like_count": book.likes_count}
        )


class AIReportViewSet(viewsets.ModelViewSet):
    serializer_class = AIReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            # 이미 존재하는 레포트가 있다면 삭제
            book_id = self.request.data.get("book")
            if not book_id:
                raise ValidationError("책 ID가 필요합니다.")

            book = get_object_or_404(Book, id=book_id)

            # 기존 레포트 삭제
            AIReport.objects.filter(user=self.request.user, book=book).delete()

            # 새 레포트 저장
            serializer.save(user=self.request.user, book=book)
        except Book.DoesNotExist:
            raise NotFound("해당 책을 찾을 수 없습니다.")
        except ValidationError as e:
            raise ValidationError(str(e))
        except Exception as e:
            print(f"Error in perform_create: {str(e)}")
            raise APIException("AI 레포트 저장 중 오류가 발생했습니다.")

    @action(detail=True, methods=["get"])
    def by_book(self, request, pk=None):
        """특정 책의 AI 레포트 조회"""
        try:
            report = AIReport.objects.get(book_id=pk, user=request.user)
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        except AIReport.DoesNotExist:
            return Response(
                {"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
