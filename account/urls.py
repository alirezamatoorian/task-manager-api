from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ProfileView

app_name = "account"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name='signup'),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("profile/", ProfileView.as_view(), name="profile")

]
