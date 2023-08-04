from __future__ import unicode_literals
from django_daraja.mpesa import utils
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime
from django.shortcuts import render, redirect
from django_daraja.views import stk_push_callback_url

from .models import Vehicle
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


@login_required()
def add_vehicle(request):
    if request.method == "POST":
        vehc_model = request.POST.get("m-name")
        vehc_horsepower = request.POST.get("h-name")
        vehc_torque = request.POST.get("t-name")
        vehc_price = request.POST.get("p-name")
        context = {"vehc_model": vehc_model,
                   "vehc_horsepower": vehc_horsepower,
                   "vehc_torque": vehc_torque,
                   "vehc_price": vehc_price,
                   "success": "Data saved successfully"
                   }
        query = Vehicle(model=vehc_model, horsepower=vehc_horsepower, torque=vehc_torque, price=vehc_price)
        query.save()
        return render(request, 'add-vehicle.html', context)
    return render(request, 'add-vehicle.html')


@login_required
def vehicles(request):
    all_vehicles = Vehicle.objects.all()
    context = {"all_vehicles": all_vehicles}
    return render(request, 'vehicles.html', context)


@login_required
def delete_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle.delete()
    messages.success(request, 'vehicle deleted successfully')
    return redirect('vehicles')


@login_required
def update_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    context = {"vehicle": vehicle}
    if request.method == "POST":
        update_model = request.POST.get('m-name')
        update_horsepower = request.POST.get('h-name')
        update_torque = request.POST.get('t-name')
        update_price = request.POST.get('p-name')
        vehicle.model = update_model
        vehicle.horsepower = update_horsepower
        vehicle.torque = update_torque
        vehicle.price = update_price
        vehicle.save()
        messages.success(request, 'Product updated successfully')
        return redirect('vehicles')
    return render(request, 'update-vehicle.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User register successfully')
            return redirect('user-registration')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def shop(request):
    all_vehicles = Vehicle.objects.all()
    context = {"all_vehicles": all_vehicles}
    return render(request, 'shop.html', context)


mpesa_client = MpesaClient()
stk_push_url = 'https:/api.darajambili.com/express-payment'


def auth_success(request):
    response = mpesa_client.access_token()
    return JsonResponse(response, safe=False)


def pay(request, id):
    vehicle = Vehicle.objects.get(id=id)
    context = {"vehicle": vehicle}
    if request.method == "POST":
        amount = request.POST.get('p-name')
        amount = int(amount)
        phone_number = request.POST.get('c-phone')
        account_ref = "PAYMENT_1"
        transaction_desc = "Paying for a product"
        transaction = mpesa_client.stk_push(phone_number, amount, account_ref, transaction_desc, stk_push_callback_url)
        return JsonResponse(transaction.response_description, safe=False)
    return render(request, 'pay.html', context)
