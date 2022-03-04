from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models.payment_type import PaymentType


class PaymentTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=1)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)
        
        self.payment_type1 = PaymentType.objects.create(
            customer=self.user1,
            merchant_name="asdf",
            acct_number=0000000000000000
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.faker = Faker()


    def test_create_payment_type(self):
        """
        Ensure we can add a payment type for a customer.
        """
        # Add product to order
        data = {
            "merchant_name": self.faker.credit_card_provider(),
            "acct_number": self.faker.credit_card_number()
        }

        response = self.client.post('/api/payment-types', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data["merchant_name"], data['merchant_name'])
        self.assertEqual(response.data["acct_number"], data['acct_number'])
        
    def test_delete_payment_type(self):
        response = self.client.delete(f'/api/payment-types/{self.payment_type1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

