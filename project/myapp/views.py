from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny

class StudentRegister(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
       
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        
        if not check_password(password, student.password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

       
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    

class UpdateDeleteStudent(APIView):
    permission_classes = [AllowAny]  
    
    def post(self, request):
       
        email = request.data.get('email')
        password = request.data.get('password')

        
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, student.password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

       
        serializer = StudentSerializer(student, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
       
        email = request.data.get('email')
        password = request.data.get('password')

       
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        
        if not check_password(password, student.password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        student.delete()
        return Response({'message': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
