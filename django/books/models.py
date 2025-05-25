from django.db import models
from django.contrib.auth.models import User

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True) 
    def __str__(self):
        return self.title
from django.contrib.auth import get_user_model
User = get_user_model()

class Thread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    read_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_threads', blank=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='threads')  # Book 모델과 연결

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='in_libraries')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username}'s library - {self.book.title}"