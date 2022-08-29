from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.account.models import ATMCard
from apps.atm.models import ATM
from apps.card_token.models import CardToken


class CardViewSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=12, required=True)
    atm_code = serializers.CharField(max_length=55, required=True)
    card_token = serializers.SerializerMethodField(method_name='get_token')

    class Meta:
        fields = ['token', 'card_number', 'atm_code']

    def validate(self, attrs):
        card_number = attrs.get('card_number')
        atm_code = attrs.get('atm_code')
        atm_card = get_object_or_404(ATMCard, number=card_number)
        atm = get_object_or_404(ATM, atm_code=atm_code)
        card_token = CardToken.objects.create(card=atm_card,atm=atm)
        return {
            'card_number': card_number,
            'card_token': card_token.key,
            'atm_code':atm_code
        }

    @staticmethod
    def get_token(obj):
        print(obj)
        return obj['card_token']
