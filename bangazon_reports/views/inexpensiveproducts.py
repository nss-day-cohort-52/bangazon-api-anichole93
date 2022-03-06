"""Module for generating games by user report"""
from re import S
from unicodedata import name
from django.shortcuts import render
from django.db import connection
from django.views import View
from bangazon_api.models import Store
from bangazon_api.models.product import Product
from bangazon_reports.views.helpers import dict_fetch_all


class InexpensiveProductList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.store_id,
                    s.id store_id,
                    s.name store_name
                FROM
                    bangazon_api_product p 
                JOIN 
                    bangazon_api_store s ON p.store_id = s.id
                WHERE p.price <= 1000
            """)

            dataset = dict_fetch_all(db_cursor)

            inexpensive_products = {}

            for row in dataset:
                product = Product()
                product.name = row["name"]
                product.price = row["price"]
                store = Store()
                store.name = row["name"]
                
                storeid = row["store_id"]
                store_name = row["store_name"]
                
                if storeid in inexpensive_products:
                    inexpensive_products[storeid]['products'].append(product)
                else:
                    inexpensive_products[storeid] = {}
                    inexpensive_products[storeid]["id"] = storeid
                    inexpensive_products[storeid]["store_name"] = store_name
                    inexpensive_products[storeid]["products"] = [product]
            
        list_of_inexpensive_products = inexpensive_products.values()
        
        template = 'list_of_inexpensive_products.html'
        context = {
            "inexpensiveproduct_list": list_of_inexpensive_products
        }

        return render(request, template, context)