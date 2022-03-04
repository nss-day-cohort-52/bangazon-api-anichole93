from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product
from bangazon_api.models.payment_type import PaymentType


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=1)
        self.user = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user)

        self.order1 = Order.objects.create(
            user=self.user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')
        

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Order.objects.count())

    def test_delete_order(self):
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

