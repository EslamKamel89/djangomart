from http.client import HTTPException

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from account.forms import (
    CreateUserForm,
    LoginForm,
    ResetUserPasswordForm,
    UpdateUserForm,
)
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress

from .token import user_tokenizer_generate


class RegisterView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("/")
        form = CreateUserForm()
        return render(request, "account/registration/register.html", {"form": form})

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
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
            messages.success(
                request,
                "Account created successfully. Please check your email to verify your account.",
            )
            return redirect(reverse("email-verification-sent"))

        messages.error(request, "Please correct the errors.")
        return render(request, "account/registration/register.html", {"form": form})


class EmailVerification(View):
    def get(self, request: HttpRequest, uidb64: str, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except Exception:
            messages.error(request, "Invalid verification link.")
            return redirect("email-verification-failed")

        if user and user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Your email has been verified successfully.")
            return redirect(reverse("email-verification-success"))

        messages.error(request, "Email verification failed or link expired.")
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
            messages.info(request, "You are already logged in.")
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
                messages.success(request, "Login successful.")
                return redirect("/")

        messages.error(request, "Invalid username or password.")
        return render(request, "account/login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        cart = request.session.get("cart")
        logout(request)
        request.session["cart"] = cart
        messages.success(request, "You have been logged out successfully.")
        return redirect("/")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "account/dashboard/dashboard.html")


class AccountDeleteView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "account/dashboard/account-delete.html")

    def post(self, request: HttpRequest):
        user = User.objects.filter(id=request.user.id)  # type: ignore
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect(reverse("dashboard"))


class AccountManagementView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        basic_form = UpdateUserForm(instance=request.user)
        password_form = ResetUserPasswordForm(request.user)
        return render(
            request,
            "account/dashboard/account-management.html",
            {"basic_form": basic_form, "password_form": password_form},
        )

    def post(self, request: HttpRequest):
        form_type = request.POST.get("type")

        basic_form = UpdateUserForm(
            request.POST if form_type == "basic" else None,
            instance=request.user,
        )
        password_form = ResetUserPasswordForm(
            request.user,
            request.POST if form_type == "password" else None,
        )

        if form_type == "basic":
            if basic_form.is_valid():
                basic_form.save()
                messages.success(request, "Account details updated successfully.")
            else:
                messages.error(request, "Failed to update account details.")
            return redirect(reverse("dashboard"))

        elif form_type == "password":
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully.")
                return redirect(reverse("dashboard"))
            messages.error(request, "Failed to update password.")
            return redirect(reverse("dashboard"))

        messages.error(request, "Invalid form submission.")
        return render(
            request,
            "account/dashboard/account-management.html",
            {"basic_form": basic_form, "password_form": password_form},
        )


class ShippingAddressView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        shipping_address: ShippingAddress | None = ShippingAddress.objects.filter(
            user=request.user
        ).first()
        form = ShippingAddressForm(instance=shipping_address)
        return render(request, "account/shipping/manage-shipping.html", {"form": form})

    def post(self, request: HttpRequest):
        shipping_address: ShippingAddress | None = ShippingAddress.objects.filter(
            user=request.user
        ).first()
        form = ShippingAddressForm(data=request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            if shipping_address is None:
                raise HTTPException("Failed to update the shipping address")
            shipping_address.user = request.user  # type: ignore
            shipping_address.save()
            messages.success(request, "Shipping address saved successfully")
            return redirect(request.path)
        messages.error(request, "Please fix the validation errors")
        return render(request, "account/shipping/manage-shipping.html", {"form": form})
