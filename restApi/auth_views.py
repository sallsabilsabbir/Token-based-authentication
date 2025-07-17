from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

import random
from django.core.mail import send_mail
from .models import PasswordResetOTP

from . serializers import RegisterSerializer, LoginSerializer,ChangePasswordSerializer, ForgotPasswordSerializer,ResetPasswordSerializer

 
from drf_spectacular.utils import extend_schema

@extend_schema(request=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public access for registration
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'msg': 'User registered successfully'})


@extend_schema(request=LoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Please provide email and password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=user.username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'msg': 'Login successful'})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# @extend_schema(request=)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require auth token to logout
def logout_user(request):
    try:
        request.user.auth_token.delete()
        return Response({"msg": "Logout successful"}, status=status.HTTP_200_OK)
    except:
        return Response({"error": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=ChangePasswordSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({'error': 'Please provide old_password and new_password'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'msg': 'Password updated successfully'}, status=status.HTTP_200_OK)


@extend_schema(request=ForgotPasswordSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    otp = str(random.randint(100000, 999999))

    # Save OTP
    PasswordResetOTP.objects.create(user=user, otp=otp)

    # Send OTP via email
    send_mail(
        subject='Your OTP for Password Reset',
        message=f'Hello {user.username},\nYour OTP for password reset is: {otp}\nIt is valid for 10 minutes.',
        from_email='sabbir@gmail.com',
        recipient_list=[email],
        fail_silently=False
    )

    return Response({'msg': 'OTP sent to your email'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_with_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not email or not otp or not new_password:
        return Response({'error': 'email, otp and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).latest('created_at')
    except PasswordResetOTP.DoesNotExist:
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    if not otp_obj.is_valid():
        return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Optionally delete OTP after use
    otp_obj.delete()

    return Response({'msg': 'Password has been reset successfully'}, status=status.HTTP_200_OK)


