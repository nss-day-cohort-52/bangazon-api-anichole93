"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from bangazon_api.models import Store
from bangazon_reports.views.helpers import dict_fetch_all


class UserStoreList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            db_cursor.execute("""
                SELECT
                    s.id,
                    s.name,
                    f.store_id,
                    f.customer_id,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    bangazon_api_store s
                JOIN 
                    bangazon_api_favorite f ON s.id = f.store_id
                JOIN
                    auth_user u ON f.customer_id = u.id
            """)

            dataset = dict_fetch_all(db_cursor)

            fav_stores_by_user = {}

            for row in dataset:
                store = Store()
                store.name = row["name"]
                
                uid = row["user_id"]
                
                if uid in fav_stores_by_user:
                    fav_stores_by_user[uid]['stores'].append(store)
                else:
                    fav_stores_by_user[uid] = {}
                    fav_stores_by_user[uid]["customer_id"] = uid
                    fav_stores_by_user[uid]["full_name"] = row["full_name"]
                    fav_stores_by_user[uid]["stores"] = [store]
            
        list_of_customers_with_fav_stores = fav_stores_by_user.values()
        
        template = 'list_with_fav_stores.html'
        context = {
            "userfavstore_list": list_of_customers_with_fav_stores
        }

        return render(request, template, context)
