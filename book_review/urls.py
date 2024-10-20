from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Library API",
      default_version='v1',
      description="API documentation for book management and reviews",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@libraryapi.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('book_review/', include("review_service.urls")),
    # API Documentation URLs
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
]
