from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User, auth
from validate_email import validate_email
from django.contrib import messages
from visualization import settings
# confimation mail
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import generateToken
from django.core.mail import EmailMessage

# Create your views here.


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldVal': request.POST,
        }
        if len(password) < 8:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/register.html', context=context)

        user = User.objects.create_user(
            username=username, password=password, email=email)
        user.is_active = False
        user.save()

        # mail sending

        current_site = get_current_site(request)
        email_subject = "Confirm Your email @VisualExpenses!!"

        message = render_to_string('authentication/email_confirmation.html', {
            'name': user.username,
            'emai': user.email,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generateToken.make_token(user),
        })
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()
        messages.success(
            request, "Account successfully created for activation confirm your mail from your accounts")
        return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST['username']
        passwaord = request.POST['password']

        user = auth.authenticate(username=username, password=passwaord)

        if user:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'Welcome ' +
                                 user.username+' you are now logged in')
                return redirect('expenses')

            messages.error(request, 'Account is not verified')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Inavlid credentials')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect('login')


class UsernameValidate(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'usernme should only conatin alphanumeric'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already taken'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidate(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Mail format is not correct'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already taken'}, status=409)
        return JsonResponse({'email_valid': True})


class EmailActivation(View):
    def get(self, request, uid64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and generateToken.check_token(user, token):
            user.is_active = True
            user.save()
            # user.auth.login(request, user)
            return render(request, "authentication/login.html")
        else:
            return render(request, "authentication/actiavtion_failed.html")
