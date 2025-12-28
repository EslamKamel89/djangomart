from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from account.forms import CreateUserForm

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
            user.email_user(subject, message)
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
