from django.urls import path, include
from .views import index, account_settings, edit_account, download_expense, download_income
urlpatterns = [
    path('', index, name="preferences"),
    path('settings', account_settings, name="account"),
    path('edit_account', edit_account, name="edit-account"),
    path('export-expense', download_expense, name="download-expense"),
    path('export-income', download_income, name="download-income")


]
