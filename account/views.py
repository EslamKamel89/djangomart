from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from account.forms import CreateUserForm


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
            user = form.save()
            login(request, user)
            return redirect("/")
        return render(request, "account/registration/register.html", {"form": form})


class EmailVerification(View):
    def get(self, request: HttpRequest): ...
class EmailVerificationSent(View):
    def get(self, request: HttpRequest): ...
class EmailVerificationSuccess(View):
    def get(self, request: HttpRequest): ...
class EmailVerificationFailed(View):
    def get(self, request: HttpRequest): ...
