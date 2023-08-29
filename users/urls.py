from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import WellViewSet, LessonAPIView, LessonDetailAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'wells', WellViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
]
