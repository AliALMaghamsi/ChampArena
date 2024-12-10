from django.shortcuts import render,redirect
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
# Create your views here.

def card_payment_view(request:HttpRequest):
    return render(request , "payment/card_input.html")