from users.models import Well, Lesson

from celery import shared_task

@shared_task
def check_payment(pk, model):
    if model == 'Well':
        instance = Well.objects.filter(pk=pk).first()
    else:
        instance = Lesson.objects.filter(pk=pk).first()

    if instance:
        prev_payment = -1
        for p in instance.payment.all():
            if prev_payment == -1:
                prev_payment = p.payment
            elif prev_payment < p.payment:
                print('Платеж не верный')
                break
