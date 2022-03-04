from rest_framework import serializers
from bangazon_api.models import Order
from bangazon_api.models import payment_type
from bangazon_api.models.payment_type import PaymentType
from .payment_type_serializer import PaymentTypeSerializer

class OrderSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer()
    class Meta:
        model = Order
        fields = ('id', 'products', 'created_on', 'completed_on', 'total', 'payment_type')
        depth = 1

class UpdateOrderSerializer(serializers.ModelSerializer):
    payment_type = serializers.IntegerField()

    class Meta:
        model = PaymentType
        fields = ('payment_type',)
