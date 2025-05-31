from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from users.views import RegisterView, PasswordResetRequestViewSet, PasswordResetConfirmViewSet


router = routers.DefaultRouter()
router.register('register', RegisterView, basename='register')
router.register('password_reset', PasswordResetRequestViewSet, basename='password_reset')
urlpatterns = [
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmViewSet.as_view({'post': 'create'}), name='password_reset_confirm'),
    path("", include(router.urls)),
]