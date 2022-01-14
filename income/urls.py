from django.urls import path
from .views import index, add_income, income_edit
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', index, name="income"),
    path('add-income', add_income, name="add_income"),
    path('income-edit/<int:id>', income_edit, name="income_edit"),
    # path('income-delete/<int:id>', expense_delete, name="income_del"),
    # path('search-income', csrf_exempt(search_expenses), name="income_search")
]
