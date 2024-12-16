from django.shortcuts import render,redirect
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import Payment
from django.http import JsonResponse
import stripe
from decimal import Decimal
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def card_payment_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("accounts:login")  # Replace "accounts:login" with your login URL name

    return render(request, "payment/card_payment.html", {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })


def process_payment_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to make a payment.")
        return redirect("accounts:login")

    if request.method == 'POST':
        try:
            
            # Retrieve the amount and payment method ID from the form
            amount = float(request.POST.get('amount', 0))
            payment_method_id = request.POST.get('payment_method_id')

            # Create a new Payment instance
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                status="Pending",
            )

            # Create a PaymentIntent using the payment method ID
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency='usd',
                payment_method=payment_method_id,
                confirm=True,  # Automatically confirm the payment
                return_url=request.build_absolute_uri('/payment/payment-success/'),  # Add return URL
            )

            # Update payment status based on the Stripe response
            payment.stripe_payment_id = intent.id
            payment.status = "Succeeded" if intent['status'] == 'succeeded' else "Failed"
            payment.save()
            request.user.profile.wallet_balance+=Decimal(amount)
            request.user.profile.save()
            if intent['status'] == 'requires_action':
                # Redirect to return_url for additional confirmation
                return JsonResponse({'redirect_url': intent['next_action']['redirect_to_url']['url']})
            elif intent['status'] == 'succeeded':
                # Update user's wallet balance after a successful payment
                # Redirect to payment success page
                return redirect("payment:payment_success")
            else:
                messages.error(request, "Payment failed. Please try again.", "alert-danger")
                return redirect("payment:card_payment_view")

        except stripe.error.CardError as e:
            messages.error(request, f"Card error: {e.user_message}", "alert-danger")
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {e.user_message}", "alert-danger")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}", "alert-danger")
        return redirect("payment:card_payment_view")

    return redirect("payment:card_payment_view")

def payment_success_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("accounts:login")  # Replace "accounts:login" with your login URL name

    return render(request, "payment/payment_success.html")

