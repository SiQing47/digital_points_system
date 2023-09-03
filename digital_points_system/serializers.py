from rest_framework import serializers

from .models import Transaction, CustomUser


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = 'original_balance', 'source', 'transaction_type', \
                 'amount', 'remaining_balance', 'description', 'timestamp'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = 'id', 'username', 'is_superuser', 'balance'
