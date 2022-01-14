import imp
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from visualization.settings import API_KEY
from expenses.models import Expense
import os
import json
from .apiCall import RealTimeCurrencyExchangeRate
from django.conf import settings
from .models import UserPrefrence
# Create your views here.


def index(request):
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    exists = UserPrefrence.objects.filter(user=request.user).exists()
    user_prefernces = None
    if exists:
        user_prefernces = UserPrefrence.objects.get(user=request.user)
    if request.method == "GET":
        return render(request, 'prefrences/index.html', {'currency': data, 'preferences': user_prefernces})
    else:
        currency = request.POST['currency']
        if exists:
            from_currency = user_prefernces.currency[:3]
            to_currency = currency[:3]
            rate = RealTimeCurrencyExchangeRate(
                from_currency, to_currency, API_KEY)
            rate = (float)(rate)
            expense = Expense.objects.filter(owner=request.user)
            for exp in expense:
                exp.amount = exp.amount*rate
                exp.save()
            user_prefernces.currency = currency
            user_prefernces.save()
        else:
            UserPrefrence.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved successfully')
        return render(request, 'prefrences/index.html', {'currency': data, 'preferences': user_prefernces})
