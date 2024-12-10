from . import views
from django.urls import path


app_name="payment"

urlpatterns=[
  path('card-payment/', views.card_payment_view, name='card_payment_view'),
]
