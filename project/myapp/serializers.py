from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'password', 'age', 'gender', 'registration_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        student = Student(
            email=validated_data['email'],
            name=validated_data['name'],
            age=validated_data['age'],
            gender=validated_data['gender']
        )
        student.set_password(validated_data['password'])  
        student.save()
        return student
