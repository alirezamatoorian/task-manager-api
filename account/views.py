from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import SignUpSerializer

User = get_user_model()


# Create your views here.


class SignUpView(CreateAPIView):
    model = User
    serializer_class = SignUpSerializer
