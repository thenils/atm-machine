import uuid

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication

from apps.card_token.models import CardToken


class GetHeader:
    def __init__(self, header_name: str):
        self.AUTHORIZATION_HEADER = header_name

    def get_authorization_header(self, request):
        """
        Return the value of entered custom headers
        """
        auth = request.META.get(self.AUTHORIZATION_HEADER, b'')

        return auth


class CardAuthenticated:
    get_header = GetHeader('HTTP_CARD_TOKEN')

    def get_card_token_object(self, request):
        auth = self.get_header.get_authorization_header(request).split()[0]
        try:
            card_token = CardToken.objects.get(key=uuid.UUID(auth).hex)
            if card_token.expireAt < timezone.now():
                card_token = None
        except:
            card_token = None

        return card_token
