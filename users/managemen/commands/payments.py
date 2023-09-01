from django.core.management.base import BaseCommand
from users.models import Payment


class Command(BaseCommand):
    help = 'Заполнение данных о платежах'

    def handle(self, *args, **kwargs):
        payment_data = [
            {
                'user': 1,
                'payment_date': '2022-01-01',
                'paid_course_or_lesson': 'Course 1',
                'payment_amount': 100.00,
                'payment_method': 'cash',
            },
            {
                'user': 2,
                'payment_date': '2022-01-02',
                'paid_course_or_lesson': 'Course 2',
                'payment_amount': 150.00,
                'payment_method': 'transfer',
            },
        ]

        for data in payment_data:
            Payment.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Данные о платежах успешно заполнены'))
