import stripe
from django.shortcuts import HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from store.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
def create_payment_intent(request):
    cart = request.data.get('cart', [])
    
    if not cart:
        return Response({'error': 'Cart is empty'}, status=400)

    net = 0
    for item in cart:
        try:
            product = Product.objects.get(id=item['id'])
        except Product.DoesNotExist:
            return Response({'error': f"Product with id {item['id']} not found."}, status=404)
        
        print("ITEM RECEIVED:", item)
        net += product.price * item['quantity']

    intent = stripe.PaymentIntent.create(
        amount=int(net),
        currency='usd',
        metadata={
            "integration_check": "accept_a_payment"
        }
    )
    return Response({"client_secret": intent.client_secret})




@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = "whsec_..."  # From Stripe dashboard

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        print("💰 Payment received!", intent['id'])

    return HttpResponse(status=200)

