from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, Review, User
from .serializers import BookSerializer, ReviewSerializer, UserSerializer, ReviewReadOnlySerializer, LoginSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .authentication import CustomJWTAuthentication
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi

def error_response(message, status_code):
    return Response({'error': message}, status=status_code)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    
     
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserSerializer,
        responses={201: "User registered successfully", 400: "Bad request"}
    )
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(f"User {user.name} saved to the database with ID {user.id}")
            print(serializer.validated_data)
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Login user to receive JWT tokens",
        request_body=LoginSerializer,
        responses={
            200: "JWT tokens (access, refresh)",
            400: "Invalid credentials",
            404: "User not found"
        }
    )
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return error_response('User not found', 404)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return error_response('Invalid credentials', 400)
        return error_response('Invalid request data', 400)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []
    authentication_classes = []
    
    @swagger_auto_schema(
        operation_description="List all books with optional filtering by book ID, title, genre, author, or year",
        manual_parameters=[
            openapi.Parameter('book_id', openapi.IN_QUERY, description="Filter by book ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by book title", type=openapi.TYPE_STRING),
            openapi.Parameter('genre', openapi.IN_QUERY, description="Filter by book genre", type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY, description="Filter by book author", type=openapi.TYPE_STRING),
            openapi.Parameter('year_of_publish', openapi.IN_QUERY, description="Filter by year of publish", type=openapi.TYPE_INTEGER)
        ],
        responses={200: BookSerializer(many=True), 404: "Books not found"}
    )
    
    def list(self, request):
        books = []
        result = []
        book_id = request.query_params.get('book_id', None)
        title = request.query_params.get('title', None)
        genre = request.query_params.get('genre', None)
        author = request.query_params.get('author', None)
        year_of_publish = request.query_params.get('year_of_publish', None)
        
        try:
            if book_id:
                books = Book.objects.filter(id=book_id)
            elif title:
                books = Book.objects.filter(title__icontains=title)
            elif genre:
                books = Book.objects.filter(genre__icontains=genre)
            elif author:
                books = Book.objects.filter(author__icontains=author)
            elif year_of_publish:
                books = Book.objects.filter(year_of_publish=year_of_publish)
            else:
                books = Book.objects.all()
            
            if not books.exists():
                return error_response('No books found', 404)
                
            result = self.serializer_class(books, many=True).data
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return error_response(str(e), 500)
        
    @swagger_auto_schema(
        operation_description="Create a new book",
        request_body=BookSerializer,
        responses={201: "Book created", 400: "Bad request"}
    )
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'  # Allows clients to set page size via query param
    max_page_size = 100
    
    
class GetReviews(APIView):
    queryset = Review.objects.all()
    serializer_class = ReviewReadOnlySerializer
    permission_classes=[]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="Retrieve reviews for a specific book, user, or rating with optional pagination",
        manual_parameters=[
            openapi.Parameter('book_id', openapi.IN_QUERY, description="Filter reviews by book ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('user_id', openapi.IN_QUERY, description="Filter reviews by user ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('rating', openapi.IN_QUERY, description="Filter reviews by rating", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size for pagination", type=openapi.TYPE_INTEGER)
        ],
        responses={200: ReviewReadOnlySerializer(many=True), 404: "Reviews not found"}
    )
    
    def get(self, request):
        result = []
        book_id = request.query_params.get('book_id', None)
        user_id = request.query_params.get('user_id', None)
        rating = request.query_params.get('rating', None)
        reviews = []
        try:
            if book_id:
                reviews = Review.objects.filter(book__id=book_id)
            elif user_id:
                reviews = Review.objects.filter(user__id = user_id)
            elif rating:
                reviews = Review.objects.filter(rating=rating)
            else:
                reviews = Review.objects.all()
                
            if not reviews.exists():
                return error_response('No reviews found', 404)
                
            result = self.serializer_class(reviews, many=True).data
            
            paginator = ReviewPagination()
            page = paginator.paginate_queryset(reviews, request)
            if page is not None:
                result = self.serializer_class(page, many=True).data
                return paginator.get_paginated_response(result)
            
            result = self.serializer_class(reviews, many=True).data
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            raise error_response(str(e), 500)
    
    
class AddReview(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    
    @swagger_auto_schema(
        operation_description="Add a new review for a book",
        request_body=ReviewSerializer,
        responses={201: "Review created", 400: "Bad request", 401: "Unauthorized"}
    )
    def post(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return error_response('Book ID is required', 400)

        # Attempt to find the book
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return error_response('Book does not exist', 404)

        # Prepare the data for the review
        data = {
            'book': book.id,
            'user': request.user.id,
            'rating': request.data.get('rating', 1),
            'comment': request.data.get('comment', '')
        }

        # Validate and create review
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
