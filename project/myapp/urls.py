from django.urls import path
from .views import  StudentRegister, UpdateDeleteStudent

urlpatterns = [
    path('register/', StudentRegister.as_view(), name='student-register'),
    path('student/', UpdateDeleteStudent.as_view(), name='student-update-delete'),
]

