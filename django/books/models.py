from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    subTitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    isbn = models.CharField(max_length=20)
    cover = models.URLField()
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()
    author = models.CharField(max_length=100)
    author_info = models.TextField()
    author_photo = models.URLField()
    customer_review_rank = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    audio_file = models.FileField(upload_to="audio/", null=True, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_books", blank=True
    )

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()


from django.contrib.auth import get_user_model

User = get_user_model()


class Thread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    read_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_threads", blank=True)
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name="threads"
    )  # Book 모델과 연결

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_comments", blank=True
    )


class UserLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="library")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="in_libraries"
    )
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user.username}'s library - {self.book.title}"


class Community(models.Model):
    CATEGORY_CHOICES = [
        ("chat", "잡담"),
        ("share", "나눔"),
        ("reading", "읽는 중"),
        ("finished", "읽은 후"),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="chat")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_posts",
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="community_posts"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_community_posts", blank=True
    )
    views = models.IntegerField(default=0)  # 조회수 필드 추가

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_popular(self):
        return self.likes.count() >= 3


class CommunityComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_comments",
    )
    post = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.writer.username} on {self.post.title}"
