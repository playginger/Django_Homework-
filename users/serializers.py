from rest_framework import serializers

from .filters import PaymentFilter
from .models import Well, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'img', 'video')


class WellSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Well
        fields = ('title', 'description', 'img', 'lessons')


# параметр `filter_set_class`, указав созданный фильтр
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        filter_set_class = PaymentFilter



