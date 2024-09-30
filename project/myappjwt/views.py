from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime
from .models import LoginLogData
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .utils import get_tokens_for_user
from rest_framework.permissions import AllowAny



class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                current_datetime = datetime.now()
                LoginLogData.objects.create(user=user, login=current_datetime, token=token['access'])
                return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
            return Response({'errors': {'non_field_errors': ['Invalid credentials']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
