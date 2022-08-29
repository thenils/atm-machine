import json

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.transaction.v1.serializer import CardViewSerializer
from apps.atm.models import ATMTransaction
from apps.atm.transaction import Transaction
from apps.card_token.authentication import CardAuthenticated
from apps.card_token.models import CardToken


class CardView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        serializer = CardViewSerializer(data=request.POST)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response({'success': False, 'message': 'something went wrong!'})


class TransactionView(viewsets.GenericViewSet):
    transaction_auth = CardAuthenticated()

    def intent_transaction(self, request, action):
        transaction_type = 'D' if action == 'withdraw' else 'C'
        card_token = self.transaction_auth.get_card_token_object(request)
        if not card_token:
            return Response({'message': 'token expired'})
        transaction = ATMTransaction.objects.create(
            type=transaction_type,
            card=card_token.card,
            atm=card_token.atm,
        )
        return Response({'status': True, 'action': action, 'transaction_id': transaction.transaction_id})

    def create(self, request, transaction_id):
        atm_transaction = get_object_or_404(ATMTransaction, transaction_id=transaction_id)
        data = json.loads(request.body)
        atm_transaction.amount = data.get('amount')
        if atm_transaction.type == 'D':
            atm_transaction.in_cash = data.get('in_cash_depo')
        atm_transaction.save()
        return Response({'success': True})

    def verify_transaction(self, request, transaction_id):
        atm_transaction = get_object_or_404(ATMTransaction, transaction_id=transaction_id)
        card_token = self.transaction_auth.get_card_token_object(request)
        if not card_token:
            return Response({'message': 'token expired'})

        if card_token.card.pin == request.POST.get('pin'):
            if atm_transaction.type == 'D':
                success, data, message = Transaction(atm_transaction.atm.in_cash, atm_transaction.atm.balance).withdraw(
                    atm_transaction.amount)
                if success:
                    with transaction.atomic():

                        atm_transaction.success = True
                        atm_transaction.status = 'SUCCESS'
                        atm_transaction.save()

                        account = atm_transaction.card.account
                        account.balance = account.balance - atm_transaction.amount
                        account.save()

                        atm_transaction.in_cash = data
                        atm = atm_transaction.atm
                        in_atm_cash = atm.in_cash
                        for k, v in data.items():
                            in_atm_cash[k] = in_atm_cash[k] - v
                        atm.in_cash = in_atm_cash
                        atm.balance = atm.balance - atm_transaction.amount
                        atm.save()

                        return Response({'success': True, 'message': 'Collect Your amount',
                                         'token_expire': self.deactivate_token(card_token)})

                return Response(
                    {'success': False, 'message': message, 'token_expire': self.deactivate_token(card_token)})
            else:
                atm_transaction.success = True
                atm_transaction.status = 'SUCCESS'
                atm_transaction.save()

                account = atm_transaction.card.account
                account.balance = account.balance + atm_transaction.amount
                account.save()

                atm = atm_transaction.atm
                in_atm_cash = atm.in_cash
                for k, v in atm_transaction.in_cash.items():
                    in_atm_cash[k] = in_atm_cash[k] + v
                atm.in_cash = in_atm_cash
                atm.balance = atm.balance + atm_transaction.amount
                atm.save()
                return Response(
                    {'success': True, 'message': 'amount will be credited to your account in next 24 hours',
                     'token_expire': self.deactivate_token(card_token)})
        return Response(
            {'success': False, 'message': 'Invalid Digit', 'token_expire': self.deactivate_token(card_token)})

    def deactivate_token(self, token: CardToken):
        token.delete()
        return True
