from django.urls import path
from .views import UserStoreList, InexpensiveProductList, ExpensiveProductList

urlpatterns = [
    path('userfavstores', UserStoreList.as_view()),
    path('inexpensiveproducts', InexpensiveProductList.as_view()),
    path('expensiveproducts', ExpensiveProductList.as_view())
]