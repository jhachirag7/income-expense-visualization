import imp
from django.shortcuts import render, redirect
from .models import Source, Income
from django.core.paginator import Paginator
from userprefrences.models import UserPrefrence
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    source = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPrefrence.objects.get(user=request.user).currency

    context = {
        'income': income,
        'page_object': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    source = Source.objects.all()
    context = {
        'source': source,
        'values': request.POST,
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        source = request.POST["source"]
        date = request.POST["date"]

        Income.objects.create(amount=amount, date=date,
                              source=source, description=description, owner=request.user)

        messages.success(request, "Record Added successfully")

        return render(request, 'income/add_income.html', context=context)

    return render(request, 'income/add_income.html', context=context)


def income_edit(request, id):
    source = Source.objects.all()
    income = Income.objects.get(pk=id)
    context = {
        'values': income,
        'sources': source
    }
    if request.method == "GET":
        return render(request, 'income/edit_income.html', context)
    else:
        amount = request.POST["amount"]
        description = request.POST["description"]
        source = request.POST["source"]
        date = request.POST["date"]
        income.owner = request.user
        income.amount = amount
        income.date = date
        income.description = description
        income.category = source
        income.save()
        messages.success(request, "expense updated successfully")
        return redirect("income")
