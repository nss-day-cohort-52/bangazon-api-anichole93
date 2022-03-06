from datetime import date, datetime
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.management.commands.seed_db import Command
import random
from bangazon_api.models import Order, Product, OrderProduct
from bangazon_api.models import payment_type
from bangazon_api.models.category import Category
from bangazon_api.models.payment_type import PaymentType
from bangazon_api.models.store import Store


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=1)
        self.user = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user)
        self.payment_type = PaymentType.objects.get(customer=self.user)
        
        self.order1 = Order.objects.create(
            user=self.user,
            payment_type=self.payment_type
        )
        # self.product1 = Product.objects.get(name="Hat")

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

    def test_complete_order(self):
        order = Order.objects.first()
        payment_type = PaymentType.objects.get(customer=order.user)
        data = {
            "created_on": order.created_on,
            "user": order.user.id,
            "completed_on": datetime.now(),
            "payment_type": payment_type.id
            }  
        response = self.client.put(f'/api/orders/{self.order1.id}/complete', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_updated = Order.objects.get(pk=order.id)
        self.assertEqual(order_updated.payment_type.id, data['payment_type'])
        
    # def test_add_product(self):
    #     product = self.client.get('/api/products/1')
    
    #     response = self.client.post(f'/api/products/{product.data["id"]}/add_to_order')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

