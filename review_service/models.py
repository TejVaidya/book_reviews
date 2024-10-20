from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) # Stores hashed password
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    @property
    def is_authenticated(self):
        return True
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    year_of_publish = models.CharField(max_length=10, null=True, blank=True)
    summary = models.TextField()
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review_book')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    rating = models.FloatField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)