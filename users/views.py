from rest_framework import viewsets, generics, filters, permissions
from rest_framework.permissions import IsAuthenticated

from .filters import PaymentFilter
from .models import Well, Lesson, Payment
from .serializers import WellSerializer, LessonSerializer, PaymentSerializer


class IsOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name='Модераторы').exists())

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Модераторы').exists()


class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            # Добавляем IsOwnerOrModerator только для создания (POST) урока
            return [IsAuthenticated(), IsOwnerOrModerator()]
        return [IsAuthenticated()]


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.BaseFilterBackend]
    ordering_fields = ['payment_date']
    filterset_class = PaymentFilter()

    def get_permissions(self):
        return [IsOwnerOrModerator()]
