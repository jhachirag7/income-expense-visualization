from datetime import date
from locale import currency
from django.contrib import messages
from django.core import paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from expenses.models import Category, Expense
from userprefrences.models import UserPrefrence
import json
from django.http import JsonResponse
import datetime
# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = "INR-Indian Rupee"
    exists = UserPrefrence.objects.filter(user=request.user).exists()
    if exists:
        currency = UserPrefrence.objects.get(user=request.user).currency
    else:
        UserPrefrence.objects.create(user=request.user, currency=currency)

    context = {
        'expense': expense,
        'page_object': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        Expense.objects.create(amount=amount, date=date,
                               category=category, description=description, owner=request.user)

        messages.success(request, "Expense Added successfully")

        return render(request, 'expenses/add_expense.html', context=context)

    return render(request, 'expenses/add_expense.html', context=context)


def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'values': expense,
        'categories': categories
    }
    if request.method == "GET":
        return render(request, 'expenses/edit_expense.html', context)
    else:
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category
        expense.save()
        messages.success(request, "expense updated successfully")
        return redirect("expenses")


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "expense deleted")
    return redirect("expenses")


def search_expenses(request):
    if request.method == "POST":
        data = json.loads(request.body)
        search_str = data["searchText"]

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        searched_data = expenses.values()
        return JsonResponse(list(searched_data), safe=False)


def category(expese):
    return expese.category


def category_amount(category, expense):
    amount = 0
    filter_by_category = expense.filter(category=category)
    for item in filter_by_category:
        amount += item.amount
    return amount


def expense_summary(request):
    todays_date = datetime.date.today()
    six_month_ago = todays_date-datetime.timedelta(days=180)
    expense = Expense.objects.filter(
        owner=request.user, date__gte=six_month_ago, date__lte=todays_date)

    finalrep = {}

    category_list = list(set(map(category, expense)))
    print(category_list)

    for x in expense:
        for y in category_list:
            print(x, y)
            finalrep[y] = category_amount(y, expense)

    print(finalrep)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
