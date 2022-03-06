"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from bangazon_api.models import Store
from bangazon_api.models.product import Product
from bangazon_reports.views.helpers import dict_fetch_all


class ExpensiveProductList(View):
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
                WHERE p.price >= 1000
            """)

            dataset = dict_fetch_all(db_cursor)

            expensive_products = {}

            for row in dataset:
                product = Product()
                product.name = row["name"]
                product.price = row["price"]
              
                storeid = row["store_id"]
                store_name = row["store_name"]
                
                if storeid in expensive_products:
                    expensive_products[storeid]['products'].append(product)
                else:
                    expensive_products[storeid] = {}
                    expensive_products[storeid]["id"] = storeid
                    expensive_products[storeid]["store_name"] = store_name
                    expensive_products[storeid]['products'] = [product]
            
        list_of_expensive_products = expensive_products.values()
        
        template = 'list_of_expensive_products.html'
        context = {
            "expensiveproduct_list": list_of_expensive_products
        }

        return render(request, template, context)