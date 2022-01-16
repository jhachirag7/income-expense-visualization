from django.urls import path
from .views import RegistrationView, UsernameValidate, EmailValidate, EmailActivation, LoginView, LogoutView, ResetPassword, PasswordConfirm
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
    path('reset-password', csrf_exempt(ResetPassword.as_view()),
         name="reset-password"),
    path('pass-activate/<uid64>/<token>',
         csrf_exempt(PasswordConfirm.as_view()), name="pass-activate"),
]
