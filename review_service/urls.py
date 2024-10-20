from django.urls import path
from .views import RegisterView, LoginView, BookViewSet, GetReviews, AddReview
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('get_reviews', GetReviews.as_view(), name='get_reviews'),
    path('add_review', AddReview.as_view(), name='add_review')
]
router.register(r'books', BookViewSet,
                basename='books')
urlpatterns += router.urls