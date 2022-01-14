from django.urls import path
from .views import RegistrationView, UsernameValidate, EmailValidate, EmailActivation, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('validate-username', csrf_exempt(UsernameValidate.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidate.as_view()),
         name="validate-email"),
    path('activate/<uid64>/<token>', EmailActivation.as_view(), name="activate"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),

]
