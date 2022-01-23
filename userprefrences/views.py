from cgitb import html
from datetime import datetime
import imp
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, response
from django.shortcuts import render
from visualization.settings import API_KEY
from expenses.models import Expense
from income.models import Income
import os
from django.template.loader import render_to_string
import csv
import json
from .apiCall import RealTimeCurrencyExchangeRate
from django.conf import settings
from .models import UserPrefrence, Profile
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


def account_settings(request):
    user = request.user
    user = User.objects.get(id=user.id)
    user_email = user.email
    exists = Profile.objects.filter(user=request.user).exists()
    Profile_user = None
    if exists:
        Profile_user = Profile.objects.get(user=request.user)
    exists = UserPrefrence.objects.filter(user=request.user).exists()
    user_prefernces = None
    if exists:
        user_prefernces = UserPrefrence.objects.get(user=request.user)
    context = {
        'email': user_email,
        'Profile': Profile_user,
        'preference': user_prefernces
    }
    return render(request, 'prefrences/account.html', context=context)


def edit_account(request):
    user = request.user
    user = User.objects.get(id=user.id)
    user_email = user.email
    exists = Profile.objects.filter(user=request.user).exists()
    Profile_user = None
    if exists:
        Profile_user = Profile.objects.get(user=request.user)
    if request.method == "GET":
        return render(request, 'prefrences/edit_account.html', {'user': Profile_user})
    else:
        name = request.POST['name']
        image = request.FILES["image"]

        if exists:
            Profile_user.name = name
            Profile_user.image = image
            Profile_user.save()
        else:
            Profile.objects.create(user=request.user, name=name, image=image)
        messages.success(request, 'Changes saved successfully')
        Profile_user = Profile.objects.get(user=request.user)
        exists = UserPrefrence.objects.filter(user=request.user).exists()
        user_prefernces = None
        if exists:
            user_prefernces = UserPrefrence.objects.get(user=request.user)
        context = {
            'email': user_email,
            'Profile': Profile_user,
            'preference': user_prefernces
        }
        return render(request, 'prefrences/account.html', context=context)


def download_expense(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expense = Expense.objects.filter(owner=request.user)

    for exp in expense:
        writer.writerow([exp.amount, exp.description, exp.category, exp.date])

    return response

def download_income(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Income'+ str(datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Source','Date'])

    income=Income.objects.filter(owner=request.user)

    for inc in income:
        writer.writerow([inc.amount,inc.description,inc.source,inc.date])

    return response