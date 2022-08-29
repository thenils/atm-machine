from django.urls import path

from apis.transaction.v1.views import CardView, TransactionView

urlpatterns = [
    path('card/', CardView.as_view(), name='fetch_card'),
    path('card/<str:action>/', TransactionView.as_view({'get': 'intent_transaction'}), name='transaction'),
    path('<str:transaction_id>/', TransactionView.as_view({'patch': 'create'}), name='transaction_amount'),
    path('<str:transaction_id>/verify/', TransactionView.as_view({'post': 'verify_transaction'}), name='verify'),
]
