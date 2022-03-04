from rest_framework import serializers
from bangazon_api.models import PaymentType
class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('id', 'obscured_num', 'merchant_name', 'customer', 'acct_number')

class CreatePaymentType(serializers.Serializer):
    acct_number = serializers.CharField()
    merchant_name = serializers.CharField()
