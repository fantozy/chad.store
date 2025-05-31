from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone

from users.serializers import (
    RegisterSerializer,
    UserSerializer,
    EmailCodeResendSerializer,
    EmailCodeConfirmSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)
from users.models import EmailVerificationCode
from users.tasks import send_email_async

import random
from datetime import timedelta

User = get_user_model()


class RegisterView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_verification_code(user)
            return Response(
                {"detail": "User registered successfully. Verification code sent to email."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user):
        code = str(random.randint(100000, 999999))

        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'created_at': timezone.now()}
        )

        subject = "Your verification code"
        message = f"Hello {user.username},\nYour verification code is: {code}"

        send_email_async.delay(subject, message, user.email)

    @action(detail=False, methods=["post"], url_path="resend_code", serializer_class=EmailCodeResendSerializer)
    def resend_code(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        existing = EmailVerificationCode.objects.filter(user=user).first()
        if existing:
            time_diff = timezone.now() - existing.created_at
            if time_diff < timedelta(minutes=1):
                wait_seconds = 60 - int(time_diff.total_seconds())
                return Response(
                    {"detail": f"Please wait {wait_seconds} seconds before requesting a new code."},
                    status=429
                )

        self.send_verification_code(user)
        return Response({"detail": "Verification code resent successfully."})

    @action(detail=False, methods=['post'], url_path='confirm_code', serializer_class=EmailCodeConfirmSerializer)
    def confirm_code(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_active = True
            user.save()
            return Response({"message": "User has been successfully activated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class PasswordResetRequestViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordResetSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"error": "User with this email does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )

            subject = 'Password Reset'
            message = f'Click the following link to reset your password: {reset_url}'

            send_email_async.delay(subject, message, user.email)

            return Response(
                {"message": "Password reset link has been sent to your email."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description="User ID (Base64 encoded)", type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description="Password reset token", type=openapi.TYPE_STRING),
        ]
    )
    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been successfully updated."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
