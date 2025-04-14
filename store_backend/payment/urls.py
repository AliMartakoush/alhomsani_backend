from django.urls import path
from .views import create_payment_intent



app_name='payment'

urlpatterns=[
    path('intent/',create_payment_intent,name='create_intent')
]