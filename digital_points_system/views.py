from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from .models import Transaction, CustomUser
from .serializers import TransactionSerializer, UserSerializer


@api_view(['POST'])
def point_transaction(request):
    required_params = ['user_id', 'source', 'amount', 'description']
    if not all(param in request.data for param in required_params):
        return Response({'message': '缺少必要的參數'}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.data.get('user_id')
    source = request.data.get('source')
    amount = request.data.get('amount')
    description = request.data.get('description')

    try:
        user = CustomUser.objects.get(id=user_id)
        origin_point = user.balance
        if 'give-points' in request.path:
            transaction_type = 'increase'
            user.balance += amount
        elif 'use-points' in request.path:
            transaction_type = 'decrease'
            if amount > user.balance:
                return Response({'error': '使用者餘額不足'}, status=status.HTTP_400_BAD_REQUEST)
            user.balance -= amount
        else:
            return Response({'error': '路徑錯誤'}, status=status.HTTP_400_BAD_REQUEST)

        user.save()

        transaction = Transaction.objects.create(
            user=user,
            transaction_type=transaction_type,
            amount=amount,
            source=source,
            description=description,
            original_balance=origin_point,
            remaining_balance=user.balance
        )
        transaction.save()

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
    except CustomUser.DoesNotExist:
        return Response({'error': '用戶不存在'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        transactions = Transaction.objects.filter(user=user)
        serializer = self.get_serializer(user)
        data = serializer.data
        data['transactions'] = TransactionSerializer(transactions, many=True).data
        return Response(data)
