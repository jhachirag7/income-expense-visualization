from django.urls import path, include
from .views import index, account_settings, edit_account
urlpatterns = [
    path('', index, name="preferences"),
    path('settings', account_settings, name="account"),
    path('edit_account', edit_account, name="edit-account"),

]
