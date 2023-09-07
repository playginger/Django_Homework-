from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import WellViewSet, LessonAPIView, LessonDetailAPIView, PaymentListAPIView

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'wells', WellViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/lessons/', LessonAPIView.as_view(), name='lesson-list'),
    path('api/lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
    # Payment
    path('payment/', PaymentListAPIView.as_view(), name='payment'),
    # маршрут для эндпоинта получения токена
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Подключить новые эндпоинты:
    path('', include(router.urls)),
]
