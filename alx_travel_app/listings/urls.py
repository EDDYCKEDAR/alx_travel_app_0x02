from django.urls import path
from .views import InitiatePaymentView, VerifyPaymentView

urlpatterns = [
    path('api/payment/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('api/payment/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
