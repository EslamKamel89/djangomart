from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from account.forms import CreateUserForm, LoginForm

from .token import user_tokenizer_generate


class RegisterView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("/")
        form = CreateUserForm()
        return render(request, "account/registration/register.html", {"form": form})

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("/")
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            user: User = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Account verification email"
            message = render_to_string(
                "account/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )
            user.email_user(subject, "Please verify your email", html_message=message)
            return redirect(reverse("email-verification-sent"))
        return render(request, "account/registration/register.html", {"form": form})


class EmailVerification(View):
    def get(self, request: HttpRequest, uidb64: str, token: str):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        if user and user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse("email-verification-success"))

        return redirect("email-verification-failed")


class EmailVerificationSent(View):
    def get(self, request: HttpRequest):
        return render(request, "account/registration/email-verification-sent.html")


class EmailVerificationSuccess(View):
    def get(self, request: HttpRequest):
        return render(request, "account/registration/email-verification-success.html")


class EmailVerificationFailed(View):
    def get(self, request: HttpRequest):
        return render(request, "account/registration/email-verification-failed.html")


class LoginView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

    def post(self, request: HttpRequest):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            messages.error(request, "Invalid username or password")
        return render(request, "account/login.html", {"form": form})


class LogoutView(View):
    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        return render(request, "account/dashboard/dashboard.html")
