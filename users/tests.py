from django.test import TestCase
from .models import Lesson, Well, Subscription
from django.contrib.auth.models import User


class LessonCRUDTest(TestCase):
    def setUp(self):
        self.well = Well.objects.create(title='Test Well')

    def test_create_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', description=self.well)
        self.assertEqual(lesson.title, 'Test Lesson')

    def test_update_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', description=self.well)
        lesson.title = 'Updated Lesson'
        lesson.save()
        self.assertEqual(lesson.title, 'Updated Lesson')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', description=self.well)
        lesson.delete()
        self.assertFalse(Lesson.objects.filter(title='Test Lesson').exists())


class SubscriptionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(user='testuser')
        self.course = Well.objects.create(title='Test Well')

    def test_subscribe_to_course(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course, subscribed=True)
        self.assertTrue(subscription.subscribed)

    def test_unsubscribe_to_course(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course, subscribed=True)
        subscription.subscribed = False
        subscription.save()
        self.assertFalse(subscription.subscribed)


