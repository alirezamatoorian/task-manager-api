from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'notifications'

router = DefaultRouter()
router.register(r'notifications',views.NotificationViewSet.as_view(),basename='notifications')


urlpatterns=[
    path("",include(router.urls)),
]