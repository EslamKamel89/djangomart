from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class RegisterView(View):
    def get(self, request: HttpRequest):
        return HttpResponse("Register")
