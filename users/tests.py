from django.test import TestCase
from rest_framework.test import APIClient
from .models import Lesson, Well, Subscription
from django.contrib.auth.models import User


class LessonCRUDTest(TestCase):
    def setUp(self):
        self.course = Well.objects.create(title='Test Course')

    def test_create_lesson(self):
        response = self.client.post('/api/lessons/', {'title': 'Test Lesson', 'course': self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.last().title, 'Test Lesson')

    def test_update_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', description=self.course)
        response = self.client.put(f'/api/lessons/{lesson.id}/', {'title': 'Updated Lesson'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lesson.objects.get(id=lesson.id).title, 'Updated Lesson')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', description=self.course)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())


class SubscriptionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.course = Well.objects.create(title='Test Course')

    def test_subscribe_to_course(self):
        self.client.force_login(self.user)
        response = self.client.post(f'/api/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course, subscribed=True).exists())

    def test_unsubscribe_to_course(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course, subscribed=True)
        self.client.force_login(self.user)
        response = self.client.post(f'/api/courses/{self.course.id}/unsubscribe/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.filter(id=subscription.id, subscribed=True).exists())
