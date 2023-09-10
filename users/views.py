from rest_framework import viewsets, generics, filters, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .filters import PaymentFilter
from .models import Well, Lesson, Payment, Subscription
from .serializers import WellSerializer, LessonSerializer, PaymentSerializer, CoursesPagination


class IsOwnerOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name='Модераторы').exists())

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Модераторы').exists()


# Представления `WellViewSet`, чтобы добавить эндпоинты для установки и удаления подписки.
class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer
    permission_classes = [IsOwnerOrModerator]
    pagination_class = CoursesPagination

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        well = self.get_object()
        Subscription.objects.get_or_create(user=request.user, course=well, subscribed=True)
        return Response({"detail": "Подписка успешно добавлена."})

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        well = self.get_object()
        Subscription.objects.filter(user=request.user, course=well).delete()
        return Response({"detail": "Подписка успешно удалена."})


class LessonAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [IsAuthenticated(), IsOwnerOrModerator()]
    #     return [IsAuthenticated()]


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser | IsOwnerOrModerator]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.BaseFilterBackend]
    ordering_fields = ['payment_date']
    filterset_class = PaymentFilter()

    def get_permissions(self):
        return [IsOwnerOrModerator()]
