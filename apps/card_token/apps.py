from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CardTokenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.card_token'
    verbose_name = _('Card Tokens')
