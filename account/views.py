from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from .serializers import SignUpSerializer, ProfileSerializer
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
