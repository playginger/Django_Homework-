from .tasks import send_email
from rest_framework.views import APIView
from rest_framework import viewsets, generics, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .filters import PaymentFilter
from .models import Well, Lesson, Payment, Subscription
from .serializers import WellSerializer, LessonSerializer, PaymentSerializer, CoursesPagination
import stripe


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

    def perform_update(self, serializer):
        updated_well = serializer.save()
        send_email.delay(updated_well.pk)


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


class PaymentListAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.BaseFilterBackend]
    ordering_fields = ['payment_date']
    filterset_class = PaymentFilter()
    permission_classes = [permissions.AllowAny]
    allowed_methods = ['GET', 'POST']

    def post_payment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stripe.api_key = "sk_test_51Npb3MC3NzfgOcvQ4K20bPJxrjAxPvWuvOpCTMkiglAUg4CsLp4bdTrfHSyn0nij6w645h1zpEEXsJP8WbiR7cCm00AxxbQlyC"
            stripe.PaymentIntent.create(
                amount=2000,
                currency="usd",
                payment_method_types=["card"]
            )
            # Действия после создания платежа
            return self.create(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentRetrieveAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    allowed_methods = ['GET', 'POST']

    def post(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51Npb3MC3NzfgOcvQ4K20bPJxrjAxPvWuvOpCTMkiglAUg4CsLp4bdTrfHSyn0nij6w645h1zpEEXsJP8WbiR7cCm00AxxbQlyC"
        payment_intent = stripe.PaymentIntent.retrieve("pi_3NpbbqC3NzfgOcvQ0ULVL8Pq")
        # Действия с полученными данными платежа
        return Response(payment_intent)
