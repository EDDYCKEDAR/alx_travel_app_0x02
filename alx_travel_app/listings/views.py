import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
import uuid
class InitiatePaymentView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        email = request.data.get('email')
        booking_reference = str(uuid.uuid4())

        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "first_name": request.data.get('first_name', 'John'),
            "last_name": request.data.get('last_name', 'Doe'),
            "tx_ref": booking_reference,
            "callback_url": "https://your-domain.com/api/payment/verify/",
            "return_url": "https://your-domain.com/payment-success/",
            "customization[title]": "Booking Payment"
        }

        response = requests.post('https://api.chapa.co/v1/transaction/initialize', json=data, headers=headers)
        res_data = response.json()

        if res_data.get('status') == 'success':
            Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                transaction_id=res_data['data']['tx_ref']
            )
            return Response({
                'checkout_url': res_data['data']['checkout_url'],
                'booking_reference': booking_reference
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': res_data}, status=status.HTTP_400_BAD_REQUEST)
class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')

        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
        }

        response = requests.get(f'https://api.chapa.co/v1/transaction/verify/{tx_ref}', headers=headers)
        res_data = response.json()

        if res_data.get('status') == 'success':
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                payment.status = 'Completed' if res_data['data']['status'] == 'success' else 'Failed'
                payment.save()
                return Response({'message': 'Payment Verified', 'status': payment.status}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': res_data}, status=status.HTTP_400_BAD_REQUEST)
