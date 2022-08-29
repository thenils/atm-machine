from django.urls import path, include

urlpatterns = [
    path('transaction/', include('apis.transaction.urls'))
]