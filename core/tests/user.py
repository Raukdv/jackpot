from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models, constants

class TestProxyUsers(TestCase):
    def setUp(self):
        normal_user = models.User.objects.create_user(
            email='test_arbitrator@gmail.com',
            password='password123',
        )

    def test_arbitrator(self):
        user = models.User.objects.get(email='test_arbitrator@gmail.com')
        self.assertIsInstance(user, models.User)
