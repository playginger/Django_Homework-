from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Lesson, Well, Subscription
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
