from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from account.forms import CreateUserForm


class RegisterView(View):
    def get(self, request: HttpRequest):
        form = CreateUserForm()
        return render(request, "account/registration/register.html", {"form": form})
