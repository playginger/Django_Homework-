from rest_framework import serializers

from .filters import PaymentFilter
from .models import Well, Lesson, Payment, Subscription

from rest_framework.pagination import PageNumberPagination

from .servises.payment import create_payment


class LessonsPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class CoursesPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'img', 'video')

    # В функции `validate` мы проверяем, что поле `video`
    # содержит ссылку только на youtube.com.
    # Если ссылка отсутствует или ссылка не является допустимой, мы возбуждаем исключение `serializers.ValidationError`.
    # Полученные данные будут проходить через эту проверку при создании или обновлении уроков.
    def validate(self, data):
        video_link = data.get('video', None)
        if video_link is not None and 'youtube.com' not in video_link:
            raise serializers.ValidationError("Недопустимая ссылка на видео.")
        return data


# Обновленный сериализатор `WellSerializer`, чтобы включить информацию о подписке текущего пользователя.
class WellSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return obj.subscriptions.filter(user=user).exists()

    class Meta:
        model = Well
        fields = ('id', 'title', 'img', 'description', 'is_subscribed')


# параметр `filter_set_class`, указав созданный фильтр
class PaymentSerializer(serializers.ModelSerializer):
    # product = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'
        filter_set_class = PaymentFilter

    def create(self, validated_data):
        payment = Payment(
            payment_amount=validated_data["payment_amount"],
            payment_method=validated_data["payment_method"],
            payment_id=create_payment(validated_data['payment_amount']),
        )
        payment.save()
        return payment


# Сериализатор `SubscriptionSerializer`, который будет использоваться для преобразования объектов подписки.
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'course', 'subscribed')
