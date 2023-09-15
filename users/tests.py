import stripe
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Lesson, Well
from users.models import User


class SubscriptionTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            telephone='800885544666',
            city='United',
            is_active=True
        )
        user.set_password('123qwe456rty')
        user.save()
        self.user = user
        self.course = Well.objects.create(title='Test Course')
        self.client = APIClient()

    def test_view_lesson(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, 200)

    def test_list_lesson(self):
        self.client.force_authenticate(self.user)
        lesson = Lesson.objects.create(title='Test Lesson', description=self.course)
        response = self.client.get(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_lesson(self):
        self.client.force_authenticate(self.user)
        lesson = Lesson.objects.create(title='Test Lesson 1', description=self.course)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, 204)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(self.user)
        data = {
            'title': 'test lesson',
            'description': 'description',
            'video': "https://youtube.com/jnikniun"
        }
        response = self.client.post("/api/lessons/", data=data)
        self.assertEqual(response.status_code, 201)


class PaymentTestCase(APITestCase):

    def test_create_payment(self, null=None):
        stripe.api_key = "sk_test_51Npb3MC3NzfgOcvQ4K20bPJxrjAxPvWuvOpCTMkiglAUg4CsLp4bdTrfHSyn0nij6w645h1zpEEXsJP8WbiR7cCm00AxxbQlyC"
        stripe.terminal.Reader.TestHelpers.present_payment_method("card")

        payment_data = [
            {
                "id": "pi_3NpbbqC3NzfgOcvQ0ULVL8Pq",
                "object": "terminal.reader",
                "action": {
                    "failure_code": null,
                    "failure_message": null,
                    "process_payment_intent": {
                        "payment_intent": "pi_3NpbbqC3NzfgOcvQ0ULVL8Pq_secret_xxarh6PuCUIA4CQBmDS4bfJrn"
                    }
                },
                "status": "succeeded",
                "type": "process_payment_intent"
            },
        ]

        url = reverse('payment')  # Путь 'payment' из файла urls.py
        response = self.client.post(url, payment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_payment(self):
        stripe.api_key = "sk_test_51Npb3MC3NzfgOcvQ4K20bPJxrjAxPvWuvOpCTMkiglAUg4CsLp4bdTrfHSyn0nij6w645h1zpEEXsJP8WbiR7cCm00AxxbQlyC"

        url = reverse('repayment')  # Путь 'repayment' из файла urls.py
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
