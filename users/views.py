from rest_framework import viewsets, generics, filters

from .filters import PaymentFilter
from .models import Well, Lesson, Payment
from .serializers import WellSerializer, LessonSerializer, PaymentSerializer


class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer


class LessonAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# параметр `filter_backends`, указывая фильтры и сортировку
class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.BaseFilterBackend]
    ordering_fields = ['payment_date']
    filterset_class = PaymentFilter
