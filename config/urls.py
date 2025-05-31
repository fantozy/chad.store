# Django Core Imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# Third-Party Imports
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="E-commerce API",
      default_version='v1',
      description="Mziuri project for E-commerce platform API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # local urls
    path("", include('products.urls')),
    path("", include('categories.urls')),
    path("", include('users.urls')),
    # JWT urls
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Swagger 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
