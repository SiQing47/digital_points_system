from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from digital_points_system.models import CustomUser, Transaction


class PointsTransactionsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='test_api_user', balance=100)

    def test_give_points_api(self):
        url = reverse('give-points')

        data = {
            'user_id': str(self.user.id),
            'source': 'TestSource',
            'type': 'increase',
            'amount': 50,
            'description': 'Test increase points'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('remaining_balance', 0), 150)

    def test_use_points_api(self):
        url = reverse('use-points')

        transaction = Transaction.objects.create(
            user=self.user,
            transaction_type='decrease',
            amount=50,
            source='TestSource',
            description='Test decrease points',
            original_balance=self.user.balance,
            remaining_balance=self.user.balance - 50
        )

        data = {
            'user_id': str(self.user.id),
            'source': 'TestSource',
            'type': 'decrease',
            'amount': 50,
            'description': 'Test decrease points'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 50)

        self.assertTrue(Transaction.objects.filter(id=transaction.id).exists())
