from django.urls import path
from .views import index, add_income, income_edit, income_delete, search_income
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', index, name="income"),
    path('add-income', add_income, name="add_income"),
    path('income-edit/<int:id>', income_edit, name="income_edit"),
    path('income-delete/<int:id>', income_delete, name="income_del"),
    path('search-income', csrf_exempt(search_income), name="income_search")
]
