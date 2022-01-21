import imp
from django.shortcuts import render, redirect
from .models import Source, Income
from django.core.paginator import Paginator
from userprefrences.models import UserPrefrence
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime
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


def income_delete(request, id):
    expense = Income.objects.get(pk=id)
    expense.delete()
    messages.success(request, "income deleted")
    return redirect("income")


def search_income(request):
    if request.method == "POST":
        data = json.loads(request.body)
        search_str = data["searchText"]

        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)

        searched_data = income.values()
        return JsonResponse(list(searched_data), safe=False)
    return redirect("income")


def stats_view(request):
    return render(request, 'income/stats.html')


def source(income):
    return income.source


def source_amount(source, income):
    amount = 0
    filter_by_source = income.filter(source=source)
    for item in filter_by_source:
        amount += item.amount
    return amount


def income_summary(request):
    todays_date = datetime.date.today()
    six_month_ago = todays_date-datetime.timedelta(days=180)
    income = Income.objects.filter(
        owner=request.user, date__gte=six_month_ago, date__lte=todays_date)

    finalrep = {}

    source_list = list(set(map(source, income)))

    for x in income:
        for y in source_list:
            finalrep[y] = source_amount(y, income)

    return JsonResponse({'income_source_data': finalrep}, safe=False)
