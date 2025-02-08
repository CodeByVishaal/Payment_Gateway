from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Products, Transactions
from .serializers import ProductSerializer, ProductUpdateSerializer
import razorpay
from django.conf import settings
class CreateOrderView(APIView):

    def post(self, request):
        try:
            amount = int(request.data.get('amount'))
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            order_data = {
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 0
            }

            order = client.order.create(order_data)

            Transactions.objects.create(
                order_id=order["id"],
                amount=request.data.get("amount")
            )

            return Response({"order_id": order["id"], "amount": amount}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class VerifyPaymentView(APIView):

    def post(self, request):
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        try:
            data = request.data
            order_id = data.get('order_id')
            payment_id = data.get('payment_id')
            signature = data.get('signature')

            is_valid = client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            if not is_valid:
                return Response({'error':'Invalid Payment Signature'}, status=status.HTTP_400_BAD_REQUEST)

            transaction = Transactions.objects.get(order_id=order_id)
            transaction.payment_id = payment_id
            transaction.status = "Paid"
            transaction.save()

            return Response({'message':'Payment Successful'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

'''
#Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def create_order(request):
    currency = 'INR'
    amount = 100

    #Create Razorpay Order
    razorpay_order = razorpay_client.order.create(amount=amount, currency=currency, payment_capture='0')
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'index.html', context)

@csrf_exempt
def payment_handler(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 100
                razorpay_client.payment_capture(payment_id, amount)
                return render(request, 'paymentSuccess.html')

            else:
                return render(request, 'paymentFailed.html')
        except Exception as e:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
'''

# Create API Views using Django REST Framework (DRF)

# GET all products (List) and POST new product (Create)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

# GET a single product (Retrieve), UPDATE, DELETE
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        print(user_id)

        try:
            return Products.objects.get(id=user_id)
        except Products.DoesNotExist:
            return Response({'error':'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({'message':'Product Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
