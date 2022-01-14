from django.urls import path
from .views import index, add_expense, expense_edit, expense_delete, search_expenses
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', index, name="expenses"),
    path('add-expense', add_expense, name="add_expenses"),
    path('expense-edit/<int:id>', expense_edit, name="expense_edit"),
    path('expense-delete/<int:id>', expense_delete, name="expense_del"),
    path('search-expense', csrf_exempt(search_expenses), name="expense_search")
]
