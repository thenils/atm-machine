from django.urls import path, include

urlpatterns = [
    path('v1/', include('apis.transaction.v1.urls'))
]