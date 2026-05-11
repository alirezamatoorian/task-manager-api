from django.template.context_processors import request
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import SignUpSerializer, ProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


# Create your views here.


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serializer = ChangePasswordSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "password change successfully"}, status=status.HTTP_200_OK)
