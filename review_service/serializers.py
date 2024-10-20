from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Review, User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # Password won't be returned in the response
    class Meta:
        model = User
        fields = ('id','name', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title', 'author', 'genre', 'year_of_publish', 'summary' )
        
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        return value
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'book', 'rating', 'comment', 'created_at')
        
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10")
        return value

class ReviewReadOnlySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    book = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ('id', 'user', 'book', 'rating', 'comment', 'created_at')
        
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10")
        return value
        
    def get_user(self, instance):
        return instance.user.name

    def get_book(self, instance):
        return instance.book.title