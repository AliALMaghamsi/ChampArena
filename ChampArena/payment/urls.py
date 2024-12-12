from . import views
from django.urls import path


app_name="payment"

urlpatterns=[
    path("card-payment/", views.card_payment_view, name="card_payment_view"),
    path("process-payment/", views.process_payment_view, name="process_payment"),
    path("payment-success/", views.payment_success_view, name="payment_success"),
]
