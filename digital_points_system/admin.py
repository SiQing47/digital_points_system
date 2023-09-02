from django.contrib import admin

from .models import CustomUser, Transaction


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'balance', 'is_superuser')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user_username', 'transaction_type', 'amount', 'source', 'description', 'timestamp']

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username'
