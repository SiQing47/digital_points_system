from rest_framework import serializers

from .models import Transaction, CustomUser


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class UserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = 'id', 'username', 'is_superuser', 'balance'
