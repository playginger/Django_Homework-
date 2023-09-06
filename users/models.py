from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    email = models.EmailField(verbose_name='почта', unique=True)
    telephone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    img = models.ImageField(verbose_name='аватар', **NULLABLE)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}, {self.telephone}, {self.city}'

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'


class Well(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    img = models.ImageField(verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    subscriptions = models.ManyToManyField(User, through='Subscription')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    img = models.ImageField(verbose_name='превью', **NULLABLE)
    video = models.URLField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


# Новая модель «Платежи»
class Payment(models.Model):
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField()
    paid_course_or_lesson = models.CharField(max_length=100)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=100, choices=payment_method_choices)

    def __str__(self):
        return f'{self.user}, {self.paid_course_or_lesson}, {self.payment_amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


# Новая модель `Subscription`
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Well, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)
