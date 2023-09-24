from datetime import timedelta

from celery.utils.time import timezone
from django.conf import settings
from django.core.mail import send_mail

from users.models import Well, User, Subscription

from celery import shared_task


@shared_task
def check_user():
    now_date = timezone.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_user = User.objects.filter(last_login__lt=one_month_ago)
    inactive_user.update(is_active=False)
    inactive_user.save()


@shared_task
def send_email(course):
    subscribers_list = Subscription.objects.filter(course=course)
    course = Well.objects.get(id=course)
    for subscriber in subscribers_list:
        # логирование
        print('Отправлено сообщение об обновлении курса')

        send_mail(
            subject="Обновление курса!",
            message=f"У курса {course.title} обновление!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email]
        )
