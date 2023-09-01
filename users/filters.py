import django_filters
from .models import Payment


# фильтры для модели `Payment'
class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.DateFromToRangeFilter()
    paid_course_or_lesson = django_filters.CharFilter(lookup_expr='содержит')
    payment_method = django_filters.CharFilter(lookup_expr='способ_оплаты')

    class Meta:
        model = Payment
        fields = ['payment_date', 'paid_course_or_lesson', 'payment_method']
