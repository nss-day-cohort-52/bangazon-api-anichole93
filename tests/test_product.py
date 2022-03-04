from itertools import product
import random
import faker_commerce
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.management.commands.seed_db import Command
from bangazon_api.models import Category
from bangazon_api.models.product import Product
from bangazon_api.models.store import Store


class ProductTests(APITestCase):
    def setUp(self):
        """
        comment
        """
        call_command('seed_db', user_count=2)
        self.user1 = User.objects.filter(store__isnull=False).first()
        self.token = Token.objects.get(user=self.user1)
        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)

        self.product1 = Product.objects.create(
                name=self.faker.ecommerce_name(),
                store=Store.objects.filter(seller_id=self.user1.id).first(),
                price=random.randint(50, 1000),
                description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam elit.",
                quantity=random.randint(2, 20),
                location=random.choice(STATE_NAMES),
                image_path="",
                category=Category.objects.get_or_create(
                    name=self.faker.ecommerce_category())[0]
            )
        
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')
        

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        category = Category.objects.first()

        data = {
            "name": self.faker.ecommerce_name(),
            "price": random.randint(50, 1000),
            "description": self.faker.paragraph(),
            "quantity": random.randint(2, 20),
            "location": random.choice(STATE_NAMES),
            "imagePath": "",
            "categoryId": category.id
        }
        response = self.client.post('/api/products', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])


    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        product = Product.objects.first()
        data = {
            "name": product.name,
            "price": product.price,
            "description": self.faker.paragraph(),
            "quantity": product.quantity,
            "location": product.location,
            "imagePath": "",
            "categoryId": product.category.id
        }
        response = self.client.put(f'/api/products/{product.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        product_updated = Product.objects.get(pk=product.id)
        self.assertEqual(product_updated.description, data['description'])

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())
        
    def test_delete_product(self):
        response = self.client.delete(f'/api/products/{self.product1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_rate_product(self):
        data = {
            "customer": self.user1.id,
            "score": random.randint(1, 5),
            "product": self.product1.id,
            "review": "blah blah blah"
        }

        response = self.client.post(f'/api/products/{self.product1.id}/rate-product', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        Command.create_ratings(self, self.user1)
        product_rated = Product.objects.get(pk=random.randint(1, Product.objects.count()))
        sum = 0
        for rating in product_rated.ratings.all():
            sum += rating.score
        avg =  sum / product_rated.ratings.count()
        
        self.assertEqual(product_rated.average_rating, avg)
