from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from digital_points_system.models import CustomUser, Transaction


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='test_api_user', balance=100)

    def test_get_user_points_api(self):
        url = reverse('user-list')

        response = self.client.get(url, {'user_id': str(self.user.id)}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('id'), str(self.user.id))
        self.assertEqual(response.data[0].get('username'), self.user.username)
        self.assertEqual(response.data[0].get('balance'), self.user.balance)

    def test_get_user_transactions_api(self):
        url = reverse('user', kwargs={'id': str(self.user.id)})

        Transaction.objects.create(
            user=self.user,
            transaction_type='increase',
            amount=50,
            source='TestSource1',
            description='Test increase points 1',
            original_balance=self.user.balance,
            remaining_balance=self.user.balance + 50
        )
        Transaction.objects.create(
            user=self.user,
            transaction_type='decrease',
            amount=25,
            source='TestSource2',
            description='Test decrease points 1',
            original_balance=self.user.balance + 50,
            remaining_balance=self.user.balance + 25
        )

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['transactions']), 2)
